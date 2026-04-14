pipeline {
    agent any

    environment {
        IMAGE_NAME = "2022bcs0064/2022bcs0064_surabhi_lab7:latest"
        CONTAINER_NAME = "ml_test_container"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh "docker pull $IMAGE_NAME"
            }
        }

        stage('Run Container') {
            steps {
                sh "docker rm -f $CONTAINER_NAME || true"
                sh "docker ps -q | xargs -r docker rm -f || true"
                sh "docker run -d -p $PORT:8000 --name $CONTAINER_NAME $IMAGE_NAME"
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                timeout(time: 60, unit: 'SECONDS') {
                    sh '''
                    until curl -s http://localhost:$PORT/; do
                      echo "Waiting for API to be ready..."
                      sleep 5
                    done
                    '''
                }
            }
        }

        stage('Valid Inference Request') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        curl -s -X POST http://localhost:$PORT/predict \
                        -H "Content-Type: application/json" \
                        -d '{"feature1":5.1,"feature2":3.5,"feature3":1.4,"feature4":0.2}'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    // Check prediction field
                    if (!response.contains("prediction")) {
                        error("❌ Prediction field missing in response")
                    }

                    // Check numeric value
                    def numeric = response.replaceAll("[^0-9.]", "")
                    if (numeric == "") {
                        error("❌ Prediction value is not numeric")
                    }
                }
            }
        }

        stage('Invalid Request Handling') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        curl -s -X POST http://localhost:$PORT/predict \
                        -H "Content-Type: application/json" \
                        -d '{"feature1":"invalid"}'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Invalid Response: ${response}"

                    // FastAPI returns "detail" for validation errors
                    if (!response.toLowerCase().contains("detail")) {
                        error("❌ Invalid input not properly handled")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh "docker rm -f $CONTAINER_NAME || true"
            }
        }
    }

    post {
        always {
            sh "docker rm -f $CONTAINER_NAME || true"
        }
        success {
            echo "✅ Pipeline Passed: Model inference validation successful"
        }
        failure {
            echo "❌ Pipeline Failed: Validation error detected"
        }
    }
}
