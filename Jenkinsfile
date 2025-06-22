pipeline {
  agent any

  environment {
    DOCKERHUB_USER = 'lamlaicuocdoi1105'
    CONFIG_REPO = 'https://github.com/danquan/simple-app-config.git'
    TAG = "${env.GIT_TAG_NAME}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          sh "docker build -t $DOCKERHUB_USER/simple-frontend:$TAG ./frontend"
          sh "docker build -t $DOCKERHUB_USER/simple-backend:$TAG ./backend"
        }
      }
    }

    stage('Push Docker Images') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh "echo $PASS | docker login -u $USER --password-stdin"
          sh "docker push $DOCKERHUB_USER/simple-frontend:$TAG"
          sh "docker push $DOCKERHUB_USER/simple-backend:$TAG"
        }
      }
    }

    stage('Update values.yaml in config repo') {
      steps {
        // sh """
        // git clone $CONFIG_REPO config-repo
        // cd config-repo/prod

        // sed -i 's|repository: .*$|repository: $DOCKERHUB_USER/simple-frontend|' values.yaml
        // sed -i 's|tag: .*$|tag: $TAG|' values.yaml

        // cd ../..
        // git config user.name "danquan"
        // git config user.email "dangquanattvhouse@gmail.com"
        // git add .
        // git commit -m "Update image tag to $TAG"
        // git push https://<token>@github.com/your-org/simple-app-config.git HEAD:main
        // """
        withCredentials([string(credentialsId: 'github-push-token', variable: 'GH_TOKEN')]) {
            sh '''
                git clone https://github.com/your-org/simple-app-config.git config-repo
                cd config-repo/prod

                # Update frontend
                sed -i 's|repository:.*simple-frontend|repository: '"$DOCKERHUB_USER"'/simple-frontend|' values.yaml
                sed -i '/frontend:/, /backend:/ s|tag:.*|tag: '"$TAG"'|' values.yaml

                # Update backend
                sed -i 's|repository:.*simple-backend|repository: '"$DOCKERHUB_USER"'/simple-backend|' values.yaml
                sed -i '/backend:/,$ s|tag:.*|tag: '"$TAG"'|' values.yaml
                
                cd ../..

                git config user.name "danquan"
                git config user.email "dangquanattvhouse@gmail.com"
                git add .
                git commit -m "Update image tag to $TAG"
                git push https://$GH_TOKEN@github.com/your-org/simple-app-config.git HEAD:main
            '''
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline completed successfully."
    }
    failure {
      echo "Pipeline failed."
    }
  }
}
