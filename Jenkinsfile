runNeighborhoodsPipeline([
    project: 'pipenv-devcheck-ci',
    tests: [
        'Unit testing': 'python -m pytest test/',
        'Linting/Style Checking': "python -m flake8 pipenv_devcheck/ test/ --max-line-length 100"
    ],
])
