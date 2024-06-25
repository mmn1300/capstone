<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convenience Table Data</title>
    <style>
        .row {
            margin-bottom: 10px;
        }
        .cell {
            display: inline-block;
            width: 150px;
        }
    </style>
</head>
<body>

    <h1>편의점 재고 정보</h1>

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

    // 쿼리 결과 확인 및 출력
    if ($result && mysqli_num_rows($result) > 0) {
        echo '<div class="row">';
        echo '<span class="cell">상품 코드</span>';
        echo '<span class="cell">상품 명</span>';
        echo '<span class="cell">수량</span>';
        echo '</div>';
        echo '<hr>';

        // 각 행을 반복하여 출력
        while ($row = mysqli_fetch_assoc($result)) {
            echo '<div class="row">';
            echo '<span class="cell">' . htmlspecialchars($row['code']) . '</span>';
            echo '<span class="cell">' . htmlspecialchars($row['cname']) . '</span>';
            echo '<span class="cell">' . htmlspecialchars($row['quantity']) . '</span>';
            echo '</div>';
        }
    } else {
        echo "<p>데이터가 없습니다.</p>";
    }

    // 데이터베이스 연결 종료
    mysqli_close($connect);
    ?>

</body>
</html>
