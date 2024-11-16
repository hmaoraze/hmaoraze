<?php
// 数据库配置
$servername = "localhost";
$username = "你的数据库用户名";
$password = "你的数据库密码";
$dbname = "你的数据库名";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 查询评论者的电子邮件地址，排除掉指定的电子邮件地址
$excluded_emails = ['hmao@blog.hsmao.cn', 'i@hmao.top', 'i@hsmao.cn'];
$excluded_emails_str = implode("', '", $excluded_emails);
$sql = "SELECT comment_author_email FROM hm_comments WHERE comment_author_email NOT IN ('$excluded_emails_str')";
$result = $conn->query($sql);

// 检查查询结果
if ($result->num_rows > 0) {
    // 使用数组去重
    $unique_emails = [];

    // 遍历查询结果，去重并写入文件
    while($row = $result->fetch_assoc()) {
        $email = $row["comment_author_email"];
        if (!in_array($email, $unique_emails)) {
            $unique_emails[] = $email;
        }
    }

    // 打开文件以写入
    $file = fopen("emails.txt", "w");

    // 输出数据到文件
    foreach ($unique_emails as $email) {
        fwrite($file, $email . "\n");
    }

    // 关闭文件
    fclose($file);
    echo "电子邮件地址已成功写入 emails.txt 文件。";
} else {
    echo "没有找到评论者电子邮件地址。";
}

// 关闭数据库连接
$conn->close();
?>