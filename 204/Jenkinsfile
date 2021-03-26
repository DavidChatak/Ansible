pipeline {
    agent { label "master"}
    environment {
        ECR_REGISTRY = "088674315177.dkr.ecr.us-east-1.amazonaws.com"
        APP_REPO_NAME = "david-repo/phonebook-app"
        AWS_REGION = "us-east-1"
        AWS_STACK_NAME = "DAVIDPHONEBOOK-${BUILD_NUMBER}"
        CFN_KEYPAIR = "NVPEM.pem"
        HOME_FOLDER = "/home/ec2-user"
        GIT_FOLDER = sh(script:'echo ${GIT_URL} | sed "s/.*\\///;s/.git$//"', returnStdout:true).trim()
        PATH=sh(script:"echo $PATH:/usr/local/bin", returnStdout:true).trim()
        APP_NAME="phonebook"
    }
    stages {
        stage ('create ECR repo') {
            steps {
                echo 'creating ECR Repository....'
                sh """
                aws ecr create-repository \
                  --repository-name ${APP_REPO_NAME} \
                  --image-scanning-configuration scanOnPush=false \
                  --image-tag-mutability MUTABLE \
                  --region ${AWS_REGION}
                """
                sh 'docker build --force-rm -t "${ECR_REGISTRY}/${APP_REPO_NAME}:latest"  . '
                sh 'docker image ls'
                script {
                    while(true){
                        echo "Docker Grand Master is not UP and running yet. Will try to reach again after 10 seconds"
                        sleep(10)
                        ip = sh(script:'aws ec2 describe-instances --region ${AWS_REGION} --filters Name=tag-value,Values=docker-grand-master Name=tag-value,Values=${AWS_STACK_NAME} --query Reservations[*].Instances[*].[PublicIpAddress] --output text | sed "s/\\s*None\\s*//g"', returnStdout:true).trim()
                        if (ip.length() >= 7) {
                            echo "Docker Grand Master Public IP Address Found: $ip"
                            env.MASTER_INSTANCE_PUBLIC_IP = "$ip"
                            break
                        } 
                    }
                }
                
            }
        }
        
        stage ("Push Docker Image to ECR Repo") {
            steps {
                echo 'Pushing App Docker Image to ECR Repo'
                sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}'
                sh 'docker push "${ECR_REGISTRY}/${APP_REPO_NAME}:latest"'
            }
        }
        stage ("Create Ifrastucture for App") {
            steps {
                echo 'Creating Docker Swarm'
                sh 'aws cloudformation create-stack --region ${AWS_REGION} --stack-name ${AWS_STACK_NAME} --capabilities CAPABILITY_IAM --template-body file://phonebook-cfn-template.yml --parameters ParameterKey=KeyPairName,ParameterValue=${CFN_KEYPAIR}'
            }
        }
        stage ("Testing thr Infrastructure") {
            steps {
               echo "Testing if Docker Swarm is ready or not by checking the Viz App on Grand Master with Public IP:${MASTER_INSTANCE_PUBLIC_IP}:8080"
                script {
                    while(true) {
                        try{
                            sh "curl -s ${MASTER_INSTANCE_PUBLIC_IP}:8080"
                            echo "Successfull connected to Viz App."
                            break
                        }
                        catch(Exception){
                            echo 'Could not connect to Viz App'
                            sleep(5)
                        }
                    }
                }
            }
        }
        stage ("deploy the App on Docker-Swarm") {
            steps {
                echo 'Deploying App on Docker-Swarm'
                environment {
                MASTER_INSTANCE_ID = sh(script:'aws ec2 describe-instances --region ${AWS_REGION} --filters Name=tag-value,Values=docker-grand-master Name=tag-value,Values=${AWS_STACK_NAME} --query Reservations[*].Instances[*].[InstanceId] --output text', returnStdout:true).trim()
                }
                echo "Cloning and Deploying App on Swarm using Grand Master with Instance Id: ${MASTER_INSTANCE_ID}"
                sh 'mssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no --region ${AWS_REGION} ${MASTER_INSTANCE_ID} git clone ${GIT_URL}'
                sleep(10)
                sh 'mssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no --region ${AWS_REGION} ${MASTER_INSTANCE_ID} docker stack deploy --with-registry-auth -c ${HOME_FOLDER}/${GIT_FOLDER}/docker-compose.yml ${APP_NAME}'
            }
        }
        
        stage ("testing app if it is deployed or not") {
            steps {
                echo 'testing app if it is deployed or not'
                script {
                    while(true) {
                        try{
                            sh "curl -s ${MASTER_INSTANCE_PUBLIC_IP}"
                            echo "Phonebook App is successfully deployed."
                            break
                        }
                        catch(Exception){
                            echo 'Could not connect to Phonebook App'
                            sleep(5)
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'deleting all local images'
            sh 'docker image prune -af'
        }
        failure {
            echo 'Deleting image repository on ECR due to failure'
            sh """
                aws ecr delete-repository \
                  --repository-name ${APP_REPO_NAME} \
                  --region ${AWS_REGION}\
                  --force
            """
            sh 'aws cloudformation delete-stack --region ${AWS_REGION} --stack-name ${AWS_STACK_NAME}'
        }
    }
}
