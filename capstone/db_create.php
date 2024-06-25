<?php
    // 데이터베이스 접속
    $connect = mysqli_connect('localhost','root','');
    $db = mysqli_select_db($connect, 'convenienceDB');

    if($db){
        echo "mysql 접속 성공<br><br>";
    }else{
        echo "데이터베이스 접속 실패";
        exit;
    }

    // 테이블 생성
    $sql = "create table convenience(
            code tinyint unsigned not null AUTO_INCREMENT PRIMARY KEY,
            cname varchar(5) not null,
            quantity smallint unsigned
            )default charset=utf8;";

    $result = mysqli_query($connect, $sql);

    if($result){
        echo "테이블 생성 성공 <br><br>";
    }else{
        echo "<hr>";
        echo "테이블 생성 실패<br><br>";
        exit;
    }

    // 데이터 삽입
    $sql = "insert into convenience values('과자',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('라면',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('마스크',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('맥주',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('면도기',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('생리대',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('생수',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('숙취해소제',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('스타킹',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('우산',0)";
    mysqli_query($connect, $sql);

    $sql = "insert into convenience values('탄산음료',0)";
    mysqli_query($connect, $sql);

    if($result){
        echo "데이터 삽입 성공<br><br>";
    }else{
        echo "<hr>";
        echo "데이터 삽입 실패";
        exit;
    }

    // 데이터베이스 접속 종료
    mysqli_close($connect);
    echo "mysql 연결 종료";
?>
