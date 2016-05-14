function main () {
    # Because the build section runs in a seperate process,
    # the path needs to be setup again
    $env:PATH = "$env:PYTHON;$env:PYTHON\\Scripts;$env:PATH"

    Write-Host "Building Package..."
    conda build --channel artplusplus .\.conda.recipe

    Write-Host "Installing Built Package for Testing..."
    conda install --channel artplusplus --use-local elemental-backend

    Write-Host "Running Tests..."
    py.test

    Write-Host "Copying Package..."
    python .\.ci\move_conda_package.py .\.conda.recipe
}

main
