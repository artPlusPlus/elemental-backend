# Sample script to install Miniconda under Windows
# Authors: Olivier Grisel, Jonathan Helmus and Kyle Kastner, Robert McGibbon
# License: CC0 1.0 Universal: http://creativecommons.org/publicdomain/zero/1.0/

$MINICONDA_URL = "http://repo.continuum.io/miniconda/"


function DownloadMiniconda ($python_version, $platform_suffix) {
    $webclient = New-Object System.Net.WebClient
    if ($python_version -match "3.5") {
        $filename = "Miniconda3-latest-Windows-" + $platform_suffix + ".exe"
    } else {
        $filename = "Miniconda-latest-Windows-" + $platform_suffix + ".exe"
    }
    $url = $MINICONDA_URL + $filename

    $basedir = $pwd.Path + "\"
    $filepath = $basedir + $filename
    if (Test-Path $filename) {
        Write-Host "Reusing" $filepath
        return $filepath
    }

    # Download and retry up to 3 times in case of network transient errors.
    Write-Host "Downloading" $filename "from" $url
    $retry_attempts = 2
    for($i=0; $i -lt $retry_attempts; $i++){
        try {
            $webclient.DownloadFile($url, $filepath)
            break
        }
        Catch [Exception]{
            Start-Sleep 1
        }
   }
   if (Test-Path $filepath) {
       Write-Host "File saved at" $filepath
   } else {
       # Retry once to get the error message if any at the last try
       $webclient.DownloadFile($url, $filepath)
   }
   return $filepath
}


function InstallMiniconda ($python_version, $architecture, $python_home) {
    Write-Host "Installing Python" $python_version "for" $architecture "bit architecture to" $python_home
    if (Test-Path $python_home) {
        Write-Host $python_home "already exists, skipping."
        return $false
    }
    if ($architecture -match "32") {
        $platform_suffix = "x86"
    } else {
        $platform_suffix = "x86_64"
    }

    $filepath = DownloadMiniconda $python_version $platform_suffix
    Write-Host "Installing" $filepath "to" $python_home
    $install_log = $python_home + ".log"
    $args = "/S /D=$python_home"
    Write-Host $filepath $args
    Start-Process -FilePath $filepath -ArgumentList $args -Wait -Passthru
    if (Test-Path $python_home) {
        $env:PATH = "$env:PYTHON;$env:PYTHON\\Scripts;$env:PATH"
        Write-Host "Python $python_version ($architecture) installation complete"
    } else {
        Write-Host "Failed to install Python in $python_home"
        Get-Content -Path $install_log
        Exit 1
    }
}


function main () {
    InstallMiniconda $env:PYTHON_VERSION $env:PYTHON_ARCH $env:PYTHON
    
    Write-Host "Configuring Conda..."
    conda config --set always_yes yes --set changeps1 no

    Write-Host "Updating Conda..."
    conda update --yes conda

    Write-Host "Installing Conda Packages..."
    $spec = "conda-build", "anaconda-client", "pytest", "pyyaml"
    conda install --yes $spec
}

main
