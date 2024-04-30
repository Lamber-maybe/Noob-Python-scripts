package main

import (
	"fmt"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"github.com/flopp/go-findfont"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"
	"sync"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"github.com/sqweek/dialog"
)

var endpath string
var cmd *exec.Cmd
var cmdMutex sync.Mutex // 用于保护 cmd 变量的互斥锁

func main() {
	myApp := app.New()
	myWindow := myApp.NewWindow("蛙老师都能使用的文件监控")
	myWindow.Resize(fyne.NewSize(800, 800))

	// 创建一个按钮，用于触发文件夹路径选择对话框
	selectButton := widget.NewButton("选择需要监控的文件夹", func() {
		showFileDialog(myWindow)
	})

	// 创建一个标签，用于显示所选的文件夹路径
	selectedPathLabel := widget.NewLabel("当前选择的文件路径: ")

	// 创建一个按钮，用于执行PowerShell命令
	executeButton := widget.NewButton("开始监控", func() {
		selectedPath := findSelectedPathLabel(myWindow).Text
		if selectedPath != "" {
			go executePowerShellCommand(endpath)
		}
	})
	// 创建一个按钮，用于关闭 PowerShell 窗口
	closeButton := widget.NewButton("结束监控", func() {
		closePowerShellWindow()
	})

	image := canvas.NewImageFromFile("./black-c.png")
	image.FillMode = canvas.ImageFillOriginal
	myWindow.SetContent(image)

	// 将按钮和标签放置在一个垂直容器中
	content := container.NewVBox(
		selectButton,
		selectedPathLabel,
		executeButton,
		closeButton,
		image,
	)

	// 设置主窗口的内容
	myWindow.SetContent(content)
	myWindow.ShowAndRun()
}

func init() {
	//设置中文字体
	fontPaths := findfont.List()
	for _, path := range fontPaths {
		if strings.Contains(path, "msyh.ttf") || strings.Contains(path, "simhei.ttf") || strings.Contains(path, "simsun.ttc") || strings.Contains(path, "simkai.ttf") {
			err := os.Setenv("FYNE_FONT", path)
			if err != nil {
				return
			}
			break
		}
	}
}

// 显示文件选择对话框
func showFileDialog(window fyne.Window) {
	filepath, _ := dialog.Directory().Title("选择监控文件").Browse()
	updateSelectedPathLabel(window, filepath)

	if filepath != "" {
		// 在这里可以处理选择的文件
		endpath = filepath
	} else {
		endpath = ""
	}
}

//// 显示文件夹路径选择对话框
//func showFolderSelectionDialog(window fyne.Window) {
//	dialog.ShowFolderOpen(func(selected fyne.ListableURI, err error) {
//		if err == nil && selected != nil {
//			selectedPath := selected.Path()
//			endpath = selectedPath
//			fmt.Println("当前选择的文件路径:", selectedPath)
//			// 更新标签显示所选的文件夹路径
//			updateSelectedPathLabel(window, selectedPath)
//			// 执行PowerShell命令
//			//executePowerShellCommand(selectedPath)
//		} else {
//			log.Println("Folder selection canceled or failed:", err)
//		}
//	}, window)
//}

// 更新标签显示所选的文件夹路径
func updateSelectedPathLabel(window fyne.Window, path string) {
	labelToUpdate := findSelectedPathLabel(window)
	if labelToUpdate != nil {
		labelToUpdate.SetText("当前选择的文件路径: " + path)
	}
}

// 查找标签部件
func findSelectedPathLabel(window fyne.Window) *widget.Label {
	content := window.Content().(*fyne.Container)
	if content == nil {
		return nil
	}

	// 遍历容器的子组件列表，查找标签部件
	for _, item := range content.Objects {
		if label, ok := item.(*widget.Label); ok {
			return label
		}
	}

	return nil
}

// 执行PowerShell命令
func executePowerShellCommand(path string) {

	cmdMutex.Lock()
	cmd = exec.Command("powershell", "-File", ".\\monitor.ps1", "-d", path)
	cmdMutex.Unlock()

	// 创建一个管道来捕获stderr输出
	stderr, err := cmd.StderrPipe()
	if err != nil {
		log.Println("Error creating stderr pipe:", err)
		return
	}

	// 启动命令
	err = cmd.Start()
	if err != nil {
		log.Println("Error starting PowerShell command:", err)
		// 设置执行策略为 Unrestricted
		setPolicyCmd := exec.Command("powershell", "-Command", "Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force")
		err := setPolicyCmd.Run()
		if err != nil {
			log.Println("Error setting execution policy:", err)
			return
		}
		return
	}

	// 读取stderr输出并将其记录到日志中
	go func() {
		log.Println("PowerShell command stderr:")
		if _, err := io.Copy(os.Stderr, stderr); err != nil {
			log.Println("Error copying stderr:", err)
		}
	}()

	// 等待命令执行完毕
	err = cmd.Wait()
	if err != nil {
		log.Println("Error executing PowerShell command:", err)
	}
}

// 关闭 PowerShell 窗口
func closePowerShellWindow() {
	if cmd != nil && cmd.Process != nil {
		// 结束 PowerShell 进程
		err := cmd.Process.Kill()
		if err != nil {
			fmt.Println("Error killing PowerShell process:", err)
			return
		}

		fmt.Println("PowerShell window closed")
	}
}
