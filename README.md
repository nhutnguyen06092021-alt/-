<!doctype html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="StudyFlow - góc học tập đơn giản và dễ dùng." />
  <title>StudyFlow — Học tập nhẹ nhàng</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="glow glow-one"></div>
  <div class="glow glow-two"></div>

  <header class="header">
    <a class="brand" href="#home" aria-label="StudyFlow - Trang chủ">
      <span class="brand-mark">S</span>
      <span>StudyFlow</span>
    </a>
    <nav aria-label="Điều hướng chính">
      <a href="#home">Trang chủ</a>
      <a href="#subjects">Môn học</a>
      <a href="#plan">Kế hoạch</a>
    </nav>
    <a class="small-button" href="#plan">Học ngay</a>
  </header>

  <main>
    <section class="hero" id="home">
      <div class="hero-copy reveal">
        <span class="eyebrow">✦ Góc học tập của bạn</span>
        <h1>Học mỗi ngày,<br><em>tiến bộ mỗi chút.</em></h1>
        <p>Một không gian nhỏ để sắp xếp môn học, theo dõi việc cần làm và giữ nhịp học thật nhẹ nhàng.</p>
        <div class="hero-actions">
          <a class="primary-button" href="#subjects">Khám phá môn học <span>→</span></a>
          <a class="text-button" href="#plan">Xem kế hoạch hôm nay</a>
        </div>
        <div class="quick-stats" aria-label="Thống kê học tập">
          <div><strong>03</strong><span>Môn đang học</span></div>
          <div><strong id="doneCount">00</strong><span>Việc hoàn thành</span></div>
          <div><strong>7 ngày</strong><span>Chuỗi học tập</span></div>
        </div>
      </div>

      <div class="hero-card reveal delay-one">
        <div class="card-top">
          <span>Tiến độ tuần này</span>
          <span class="status-dot">Đang tốt</span>
        </div>
        <div class="focus-ring">
          <div><strong id="ringPercent">0%</strong><span>hoàn thành</span></div>
        </div>
        <div class="week-bars" aria-label="Số phiên học trong tuần">
          <div><i style="--height: 42%"></i><span>T2</span></div>
          <div><i style="--height: 64%"></i><span>T3</span></div>
          <div><i style="--height: 50%"></i><span>T4</span></div>
          <div><i style="--height: 82%"></i><span>T5</span></div>
          <div><i style="--height: 68%"></i><span>T6</span></div>
          <div><i style="--height: 35%"></i><span>T7</span></div>
          <div><i style="--height: 18%"></i><span>CN</span></div>
        </div>
      </div>
    </section>

    <section class="section" id="subjects">
      <div class="section-heading reveal">
        <div>
          <span class="eyebrow">Môn học</span>
          <h2>Hôm nay học gì?</h2>
        </div>
        <p>Chọn một môn và bắt đầu bằng mục tiêu nhỏ.</p>
      </div>

      <div class="subject-grid">
        <article class="subject-card purple reveal">
          <div class="subject-icon">∑</div>
          <span class="tag">Tư duy</span>
          <h3>Toán học</h3>
          <p>Ôn lại kiến thức và luyện bài tập theo từng chủ đề.</p>
          <div class="card-progress"><i style="width: 68%"></i></div>
          <footer><span>68% hoàn thành</span><button aria-label="Mở môn Toán">→</button></footer>
        </article>

        <article class="subject-card blue reveal delay-one">
          <div class="subject-icon">&lt;/&gt;</div>
          <span class="tag">Thực hành</span>
          <h3>Lập trình</h3>
          <p>Học nền tảng web qua những dự án ngắn và dễ hiểu.</p>
          <div class="card-progress"><i style="width: 52%"></i></div>
          <footer><span>52% hoàn thành</span><button aria-label="Mở môn Lập trình">→</button></footer>
        </article>

        <article class="subject-card orange reveal delay-two">
          <div class="subject-icon">Aa</div>
          <span class="tag">Ngôn ngữ</span>
          <h3>Tiếng Anh</h3>
          <p>Mỗi ngày một ít từ vựng, nghe và giao tiếp thực tế.</p>
          <div class="card-progress"><i style="width: 74%"></i></div>
          <footer><span>74% hoàn thành</span><button aria-label="Mở môn Tiếng Anh">→</button></footer>
        </article>
      </div>
    </section>

    <section class="section plan-section" id="plan">
      <div class="plan-copy reveal">
        <span class="eyebrow">Kế hoạch hôm nay</span>
        <h2>Ba việc nhỏ là đủ.</h2>
        <p>Đánh dấu từng việc khi hoàn thành. Tiến độ được lưu ngay trên trình duyệt của bạn.</p>
        <div class="total-progress"><i id="totalProgress"></i></div>
        <span class="progress-label" id="progressLabel">0/3 nhiệm vụ hoàn thành</span>
      </div>

      <div class="task-list reveal delay-one">
        <label class="task">
          <input type="checkbox" data-task="math" />
          <span class="check"></span>
          <span><strong>Làm 10 bài Toán</strong><small>30 phút · Đại số</small></span>
          <b>08:30</b>
        </label>
        <label class="task">
          <input type="checkbox" data-task="code" />
          <span class="check"></span>
          <span><strong>Hoàn thành bài HTML</strong><small>45 phút · Lập trình web</small></span>
          <b>14:00</b>
        </label>
        <label class="task">
          <input type="checkbox" data-task="english" />
          <span class="check"></span>
          <span><strong>Ôn 20 từ mới</strong><small>20 phút · Tiếng Anh</small></span>
          <b>20:00</b>
        </label>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="brand"><span class="brand-mark">S</span><span>StudyFlow</span></div>
    <p>Học nhẹ nhàng, tiến bộ bền vững.</p>
    <span>© 2026 StudyFlow</span>
  </footer>

  <script src="app.js"></script>
</body>
</html>
