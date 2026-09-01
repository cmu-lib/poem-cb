function copyToClipboard(text) {
          navigator.clipboard.writeText(text).then(() => {
              // console.log('Copied to clipboard');
              document.getElementById('copyCitationButt').innerText = 'Copied!';
          }).catch(err => {
              console.error('Failed to copy:', err);
          });
      }