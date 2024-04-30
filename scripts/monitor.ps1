
"""
Summary:

.\monitor.ps1 -d xxxxxx

powershell脚本，监控指定文件目录下，新增，删除，修改clip文件，并windows toast弹窗

"""

param(
    [string]$directoryPath
)

if (-not $directoryPath) {
    Write-Host "Usage: .\monitor.ps1 -d path"
    exit
}

# 设置要监控的文件夹路径
$global:folderPath = $directoryPath


# 创建FileSystemWatcher对象
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $global:folderPath
$watcher.Filter = "*.clip";
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

# 监听文件夹事件
Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action {
    $path = $Event.SourceEventArgs.FullPath
    $date = Get-Date -Format "yyyy-MM-dd"
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    
    $fileName = "$date-Created.txt"
    Write-Output "$time - Created: $path" | Out-File -FilePath $fileName -Append

    Write-Host "$time - Created: $path"


# 创建消息通知
$headlineText = "$time - Created."
$bodyText = "$path"

$xml = @"
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>${headlineText}</text>
      <text>${bodyText}</text>
    </binding>
  </visual>
  <actions>
    <action content="Open Folder" activationType="protocol" arguments="file:///${global:folderPath}" />
  </actions>
</toast>
"@
$XmlDocument = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]::New()
$XmlDocument.loadXml($xml)
$AppId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::CreateToastNotifier($AppId).Show($XmlDocument)

}

Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action {
    $path = $Event.SourceEventArgs.FullPath
    $date = Get-Date -Format "yyyy-MM-dd"
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    $fileName = "$date-Changed.txt"
    Write-Output "$time - Changed: $path" | Out-File -FilePath $fileName -Append

    Write-Host "$time - Modified: $path"
}

Register-ObjectEvent -InputObject $watcher -EventName "Deleted" -Action {
    $path = $Event.SourceEventArgs.FullPath
    $date = Get-Date -Format "yyyy-MM-dd"
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    $fileName = "$date-Deleted.txt"
    Write-Output "$time - Deleted: $path" | Out-File -FilePath $fileName -Append

    Write-Host "$time - Deleted: $path"
}

Write-Host "Monitoring folder: $global:folderPath"
Write-Host "Press Ctrl+C to stop monitoring..."

# 等待用户按下Ctrl+C以停止监视
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    $watcher.Dispose()
}
