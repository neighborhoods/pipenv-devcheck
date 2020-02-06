pipeline {
    agent { dockerfile true }
    stages{
        stage('Unit Testing') {
            steps {
                sh 'python -m pytest'
            }
        }
        stage('Linting/Style Checking') {
            steps {
                sh 'python -m flake8'
            }
        }

    }
}
