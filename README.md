<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .badge { margin-right: 5px; }
    </style>
</head>
<body>

<h1>Library Management System</h1>

<p>
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" class="badge">
    <img src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" class="badge">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" class="badge">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" class="badge">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" class="badge">
</p>

<p>A simple yet powerful library management system built with Flask, MySQL, and a straightforward HTML/CSS/JavaScript front end. This project demonstrates a full-stack application that allows users to manage books and user records efficiently.</p>

<h2>Features</h2>
<ul>
    <li>User management: Add, update, and delete users.</li>
    <li>Book management: Add, update, and delete books.</li>
    <li>Borrowing system: Users can borrow and return books.</li>
    <li>Real-time updates: Front-end updates without page reloads.</li>
</ul>

<h2>Installation</h2>
<p>To get this project up and running, you'll need to follow these steps:</p>
<ol>
    <li><strong>Clone the repository:</strong><br>
        <code>git clone https://github.com/nixxxxe/FinalProj.git<br>
        cd FinalProj</code>
    </li>
    <li><strong>Set up a virtual environment (optional but recommended):</strong><br>
        <code>python -m venv venv<br>
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code>
    </li>
    <li><strong>Install the requirements:</strong><br>
        <code>pip install -r requirements.txt</code>
    </li>
    <li><strong>Set up MySQL:</strong>
        <ul>
            <li>Create a new MySQL database.</li>
            <li>Import the <code>schema.sql</code> file.</li>
        </ul>
    </li>
    <li><strong>Configure the application:</strong>
        <ul>
            <li>Edit the <code>main.py</code> file to set your database credentials.</li>
        </ul>
    </li>
</ol>

<h2>Usage</h2>
<p>To run the application:</p>
<code>flask run</code>
<p>Navigate to <a href="http://localhost:5000">http://localhost:5000</a> in your web browser to view the application.</p>

<h2>Contributing</h2>
<p>Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are <strong>greatly appreciated</strong>.</p>
<ol>
    <li>Fork the Project</li>
    <li>Create your Feature Branch (<code>git checkout -b feature/AmazingFeature</code>)</li>
    <li>Commit your Changes (<code>git commit -m 'Add some AmazingFeature'</code>)</li>
    <li>Push to the Branch (<code>git push origin feature/AmazingFeature</code>)</li>
    <li>Open a Pull Request</li>
</ol>

<h2>License</h2>
<p>Distributed under the MIT License. See <code>LICENSE</code> for more information.</p>

<h2>Contact</h2>
<p>Your Name - <a href="https://twitter.com/your_twitter">@your_twitter</a> - email@example.com</p>
<p>Project Link: <a href="https://github.com/nixxxxe/FinalProj">https://github.com/nixxxxe/FinalProj</a></p>

</body>
</html>
