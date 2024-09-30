# Check if pandoc is installed
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "pandoc could not be found. Please install it first."
    Exit
}

# Convert each .md file to .docx
Get-ChildItem -Filter *.md | ForEach-Object {
    $outputFile = [System.IO.Path]::ChangeExtension($_.FullName, "docx")
    Write-Host "Converting $($_.Name) to $([System.IO.Path]::GetFileName($outputFile))"
    pandoc -f markdown -t docx -o $outputFile $_.FullName
}

Write-Host "Conversion complete!"