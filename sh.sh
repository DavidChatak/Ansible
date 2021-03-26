 if [ -z "$(ls -al /var/www/html | grep .git)" ]; then
          sudo git clone https://github.com/kodekloudhub/learning-app-ecommerce.git /var/www/html/
          echo "ok"
        else
          echo "already cloned..."
        fi
