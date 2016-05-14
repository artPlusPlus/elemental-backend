function UploadToAnacondaCloud () {
    # Because the build section runs in a seperate process,
    # the path needs to be setup again
    $env:PATH = "$env:PYTHON;$env:PYTHON\\Scripts;$env:PATH"

    Write-Host "Uploading to Anaconda Cloud..."
    if ($env:APPVEYOR_REPO_BRANCH -eq "master") {
        python .\.ci\anaconda_upload.py "main"
    }
    else {
        python .\.ci\anaconda_upload.py "dev"
    }
}


function main () {
    UploadToAnacondaCloud
}

main
