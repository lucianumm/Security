$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = if ($args.Count -gt 0) { $args[0] } else { '.' }
$pythonLauncher = Get-Command -Name 'python3', 'python', 'py' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -eq $pythonLauncher) {
    [Console]::Out.WriteLine('{"result":"ERROR","reason":"Python 3.9+ is required"}')
    exit 2
}
$pythonArguments = @()
if ($pythonLauncher.Name -eq 'py.exe' -or $pythonLauncher.Name -eq 'py') {
    $pythonArguments += '-3'
}
$pythonArguments += @((Join-Path $scriptDirectory 'security_auditor.py'), 'gate', '--root', $projectRoot)
& $pythonLauncher.Source @pythonArguments
exit $LASTEXITCODE
