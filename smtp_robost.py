import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

# 读取用户邮箱列表
def read_emails_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        emails = f.readlines()
    emails = [email.strip() for email in emails if email.strip()]
    return emails

# 初始化发件邮箱账号信息
email_account = "你的邮件"
email_password = "你的邮件密码"
smtp_server = "你的邮件服务器地址"
smtp_port = 465

# 构建邮件内容
def build_email(user_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = email_account
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    return msg

# 发送邮件
def send_email(user_email, subject, message):
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_account, email_password)
        msg = build_email(user_email, subject, message)
        server.sendmail(email_account, user_email, msg.as_string())
        server.quit()
        print(f"已发送用户协议更新通知邮件给：{user_email}")
        return True
    except Exception as e:
        print(f"发送邮件给 {user_email} 时发生错误: {str(e)}")
        return False

# 选择文件并发送邮件
def select_and_send_emails():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        messagebox.showwarning("警告", "未选择文件")
        return

    user_emails = read_emails_from_file(file_path)
    if not user_emails:
        messagebox.showwarning("警告", "文件中没有有效的邮箱地址")
        return

    success_count = 0
    failure_count = 0

    for user_email in user_emails:
        if send_email(user_email, subject, message):
            success_count += 1
        else:
            failure_count += 1

    messagebox.showinfo("结果", f"邮件发送完成。\n成功发送: {success_count}\n发送失败: {failure_count}")

# 构建邮件内容
subject = "关于用户协议更新的通知"
message = """
尊敬的用户，您好！

我们最近更新了我们的用户协议。请花几分钟时间阅读新的条款，以了解任何可能影响您的更改。

您可以在这里查看最新的用户协议：
[https://blog.hsmao.cn/hmao-diary-privacy-policy]

如果您有任何疑问或需要进一步的帮助，请随时联系我们。

感谢您的理解和支持！

此致
hmao的日记
"""

# 创建 GUI 界面
def create_gui():
    root = tk.Tk()
    root.title("发送用户协议更新通知邮件")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="请选择包含用户邮箱的 TXT 文件")
    label.pack(pady=5)

    button = tk.Button(frame, text="选择文件并发送邮件", command=select_and_send_emails)
    button.pack(pady=10)

    root.mainloop()

# 运行 GUI 界面
create_gui()