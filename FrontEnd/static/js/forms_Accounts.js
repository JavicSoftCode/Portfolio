document.addEventListener('DOMContentLoaded', function () {
            const inputs = document.querySelectorAll('.form-group input');
            inputs.forEach(input => {
                input.addEventListener('focus', function () {
                    input.nextElementSibling.style.top = '3px';
                    input.nextElementSibling.style.left = '16px';
                    input.nextElementSibling.style.fontSize = '22px';
                    input.nextElementSibling.style.color = '#000';
                    input.nextElementSibling.style.backgroundColor = 'white';
                    input.nextElementSibling.style.padding = '0 3px';
                    input.nextElementSibling.style.borderRadius = '4px';
                });
                input.addEventListener('blur', function () {
                    if (input.value === '') {
                        input.nextElementSibling.style.top = '50%';
                        input.nextElementSibling.style.fontSize = '20px';
                        input.nextElementSibling.style.color = '#000';
                        input.nextElementSibling.style.backgroundColor = 'transparent';
                        input.nextElementSibling.style.padding = '0';
                        input.nextElementSibling.style.borderRadius = '0';
                    }
                });
                if (input.value !== '') {
                    input.nextElementSibling.style.top = '10px';
                    input.nextElementSibling.style.left = '16px';
                    input.nextElementSibling.style.fontSize = '20px';
                    input.nextElementSibling.style.color = '#000';
                    input.nextElementSibling.style.backgroundColor = 'white';
                    input.nextElementSibling.style.padding = '0 3px';
                    input.nextElementSibling.style.borderRadius = '4px';
                }
            });
        });