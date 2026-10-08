param([Parameter(Mandatory = $true)][string]$Godot)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$engine = (Resolve-Path -LiteralPath $Godot).Path
$tempBase = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$testRoot = Join-Path $tempBase ('godot-toolkit-smoke-' + [guid]::NewGuid().ToString('N'))
$project = Join-Path $testRoot 'project'
$data = Join-Path $testRoot 'data'

try {
    New-Item -ItemType Directory -Path $project, $data -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'project.godot') -Destination $project
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'smoke_test.gd') -Destination $project
    Copy-Item -LiteralPath (Join-Path $repo 'templates') -Destination $project -Recurse

    $importOutput = & $engine --headless --path $project --editor --import 2>&1
    if ($LASTEXITCODE -ne 0 -or (($importOutput -join "`n") -match 'SCRIPT ERROR')) {
        $importOutput | Write-Output
        throw 'Godot import failed.'
    }
    $result = & $engine --headless --path $project --script 'res://smoke_test.gd' -- "--test-dir=$data" 2>&1
    $output = $result -join "`n"
    $output | Write-Output
    if ($LASTEXITCODE -ne 0 -or $output -match 'SCRIPT ERROR' -or $output -notmatch 'TOOLKIT_SMOKE: OK') {
        throw 'Toolkit smoke test failed.'
    }
}
finally {
    $resolvedRoot = [IO.Path]::GetFullPath($testRoot)
    if ($resolvedRoot.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and
        [IO.Path]::GetFileName($resolvedRoot).StartsWith('godot-toolkit-smoke-', [StringComparison]::Ordinal) -and
        (Test-Path -LiteralPath $resolvedRoot)) {
        Remove-Item -LiteralPath $resolvedRoot -Recurse -Force
    }
}
