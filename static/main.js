// 로그인 여부 확인 함수
function checkLogin(targetUrl) {
    fetch('/api/check-login')
        .then(response => response.json())
        .then(data => {
            if (data.is_logged_in) {
                window.location.href = targetUrl;
            } else {
                if (confirm("로그인이 필요합니다. 로그인하시겠습니까?")) {
                    window.location.href = '/login_selection';
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

// 이미지 미리보기
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('preview').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        document.getElementById('preview').src = "static/images/image.png";
    }
}
