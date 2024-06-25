<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submitted Data</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>

    <h1>상품 등록</h1>

    <?php

    // 데이터베이스에 연결
    $connect = mysqli_connect('localhost', 'root', '', 'convenienceDB');

    // 데이터베이스 연결 확인
    if (!$connect) {
        die("MySQL 접속 실패: " . mysqli_connect_error());
    }

    // SQL 쿼리 실행
    $sql = "SELECT * FROM convenience";
    $result = mysqli_query($connect, $sql);

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $texts = $_POST['text'];
        $numbers = $_POST['number'];

            // 쿼리 결과 확인 및 출력
        if ($result && mysqli_num_rows($result) > 0) {
            // 각 행을 반복하여 출력
            while ($row = mysqli_fetch_assoc($result)) {

                for($i=0;$i<count($texts);$i++){
                    if($texts[$i] == $row['cname']){
                        $cname = $row['cname'];
                        $number = $row['quantity'] + $numbers[$i];
                        $sql = "update convenience set quantity =".$number." where cname = '".$texts[$i]."'";
                        mysqli_query($connect, $sql);
                    }
                }
            }
            echo "<p>데이터가 정상적으로 입력되었습니다.</p>";
        } else {
            echo "<p>데이터가 없습니다.</p>";
        }
        

    } else {
        echo "<p>Invalid request method.</p>";
    }

        // 데이터베이스 연결 종료
        mysqli_close($connect);
    ?>

    <button id="backToPage">이전 페이지로</button>

    <script>
        document.getElementById('backToPage').addEventListener('click', function() {
            window.location.href = 'third_page.html';  // 버튼을 눌렀을 때 이동할 URL
        });
    </script>

</body>
</html>
