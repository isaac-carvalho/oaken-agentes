<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oaken IA - Agentes de IA para WhatsApp Business</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
--primary:#106EBE;
--accent:#0FFCBE;
--bg-dark:#0a1628;
--bg-card:#0f1f3a;
--bg-card-hover:#132848;
--bg-section:#0c1a30;
--text-primary:#f0f4f8;
--text-secondary:#a0b4cc;
--text-muted:#6b82a0;
--border-color:#1a3055;
--gradient-blue:linear-gradient(135deg,#106EBE,#0FFCBE);
--gradient-subtle:linear-gradient(135deg,#0f1f3a,#132848);
--radius-lg:12px;
--radius-sm:8px;
--radius-pill:999px;
}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:'Inter',sans-serif;background:var(--bg-dark);color:var(--text-primary);line-height:1.6;overflow-x:hidden}
h1,h2,h3,h4,h5,h6{font-family:'DM Sans',sans-serif;font-weight:800;line-height:1.15}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
a{text-decoration:none;color:inherit}

/* ===== UTILITY ===== */
.gradient-text{background:var(--gradient-blue);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.accent-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--accent);margin-right:10px;flex-shrink:0}
.btn-primary{
display:inline-flex;align-items:center;gap:8px;
padding:14px 32px;border-radius:var(--radius-pill);
background:var(--gradient-blue);color:#0a1628;
font-family:'DM Sans',sans-serif;font-weight:700;font-size:.95rem;
border:none;cursor:pointer;transition:all .3s;
box-shadow:0 4px 24px rgba(15,252,190,.2);
}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(15,252,190,.35)}
.btn-outline{
display:inline-flex;align-items:center;gap:8px;
padding:14px 32px;border-radius:var(--radius-pill);
background:transparent;color:var(--accent);
font-family:'DM Sans',sans-serif;font-weight:700;font-size:.95rem;
border:2px solid var(--accent);cursor:pointer;transition:all .3s;
}
.btn-outline:hover{background:rgba(15,252,190,.1);transform:translateY(-2px)}
.section-label{
display:inline-flex;align-items:center;gap:8px;
padding:6px 16px;border-radius:var(--radius-pill);
background:rgba(15,252,190,.08);border:1px solid rgba(15,252,190,.2);
color:var(--accent);font-size:.8rem;font-weight:600;
text-transform:uppercase;letter-spacing:1.5px;
margin-bottom:16px;
}
.section-title{font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:16px}
.section-sub{color:var(--text-secondary);font-size:1.05rem;max-width:600px;margin:0 auto 48px}
section{padding:100px 0;position:relative}

/* ===== REVEAL ===== */
.reveal{opacity:0;transform:translateY(30px);transition:opacity .7s ease,transform .7s ease}
.reveal.visible{opacity:1;transform:translateY(0)}

/* ===== DECORATIVE ===== */
.deco-circle{position:absolute;border-radius:50%;pointer-events:none;opacity:.06}
.deco-circle.c1{width:500px;height:500px;background:var(--accent);top:-200px;right:-150px;filter:blur(120px)}
.deco-circle.c2{width:400px;height:400px;background:var(--primary);bottom:-150px;left:-100px;filter:blur(100px)}

/* ===== NAV ===== */
.navbar{
position:fixed;top:0;left:0;right:0;z-index:1000;
padding:16px 0;transition:all .3s;
background:rgba(10,22,40,.7);backdrop-filter:blur(20px);
border-bottom:1px solid transparent;
}
.navbar.scrolled{border-bottom-color:var(--border-color);background:rgba(10,22,40,.95)}
.nav-inner{display:flex;align-items:center;justify-content:space-between}
.nav-logo{font-family:'DM Sans',sans-serif;font-weight:800;font-size:1.5rem;display:flex;align-items:center;gap:8px}
.nav-logo .logo-icon{
width:36px;height:36px;border-radius:var(--radius-sm);
background:var(--gradient-blue);display:flex;align-items:center;justify-content:center;
font-size:1.1rem;font-weight:800;color:#0a1628;
}
.nav-links{display:flex;align-items:center;gap:32px;list-style:none}
.nav-links a{color:var(--text-secondary);font-size:.9rem;font-weight:500;transition:color .3s;position:relative}
.nav-links a:hover{color:var(--accent)}
.nav-links a::after{content:'';position:absolute;bottom:-4px;left:0;width:0;height:2px;background:var(--accent);transition:width .3s}
.nav-links a:hover::after{width:100%}
.nav-cta{
padding:10px 24px;border-radius:var(--radius-pill);
background:var(--gradient-blue);color:#0a1628;
font-weight:700;font-size:.85rem;transition:all .3s;
}
.nav-cta:hover{box-shadow:0 4px 20px rgba(15,252,190,.3);transform:translateY(-1px)}
.hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px}
.hamburger span{display:block;width:24px;height:2px;background:var(--text-primary);border-radius:2px;transition:all .3s}
.mobile-menu{
display:none;position:fixed;top:0;left:0;right:0;bottom:0;
background:rgba(10,22,40,.98);z-index:999;
flex-direction:column;align-items:center;justify-content:center;gap:32px;
}
.mobile-menu.active{display:flex}
.mobile-menu a{font-family:'DM Sans',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text-primary)}
.mobile-close{position:absolute;top:24px;right:24px;background:none;border:none;color:var(--text-primary);font-size:2rem;cursor:pointer}

/* ===== HERO ===== */
.hero{padding:140px 0 100px;position:relative;overflow:hidden;min-height:100vh;display:flex;align-items:center}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
.hero-badge{
display:inline-flex;align-items:center;gap:8px;
padding:8px 18px;border-radius:var(--radius-pill);
background:rgba(15,252,190,.08);border:1px solid rgba(15,252,190,.2);
color:var(--accent);font-size:.82rem;font-weight:600;margin-bottom:24px;
}
.hero-badge .pulse{width:8px;height:8px;border-radius:50%;background:var(--accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.5)}}
.hero h1{font-size:clamp(2rem,4.5vw,3.2rem);margin-bottom:20px;line-height:1.1}
.hero h1 .highlight{color:var(--accent);position:relative}
.hero-sub{color:var(--text-secondary);font-size:1.1rem;margin-bottom:32px;max-width:480px}
.hero-buttons{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:40px}
.hero-social-proof{display:flex;align-items:center;gap:16px}
.avatar-stack{display:flex}
.avatar-stack .av{
width:36px;height:36px;border-radius:50%;
border:2px solid var(--bg-dark);margin-left:-10px;
display:flex;align-items:center;justify-content:center;
font-size:.7rem;font-weight:700;
}
.avatar-stack .av:first-child{margin-left:0}
.avatar-stack .av:nth-child(1){background:linear-gradient(135deg,#106EBE,#0ca89e)}
.avatar-stack .av:nth-child(2){background:linear-gradient(135deg,#0FFCBE,#08a87e)}
.avatar-stack .av:nth-child(3){background:linear-gradient(135deg,#1a8cee,#106EBE)}
.avatar-stack .av:nth-child(4){background:linear-gradient(135deg,#0FFCBE,#106EBE)}
.social-text{font-size:.85rem;color:var(--text-secondary)}
.social-text strong{color:var(--accent);font-weight:700}

/* Phone mockup */
.phone-wrapper{position:relative;display:flex;justify-content:center}
.phone-mockup{
width:300px;height:580px;background:#111;border-radius:36px;
padding:12px;position:relative;
border:3px solid #2a2a2a;
box-shadow:0 30px 80px rgba(0,0,0,.5),0 0 60px rgba(15,252,190,.08);
}
.phone-screen{
width:100%;height:100%;border-radius:26px;overflow:hidden;
background:linear-gradient(180deg,#075e54 0%,#075e54 8%,#0b141a 8%,#0b141a 100%);
display:flex;flex-direction:column;
}
.phone-header{
padding:10px 16px;background:#075e54;display:flex;align-items:center;gap:10px;
}
.phone-header .back-arrow{color:#fff;font-size:.9rem}
.phone-header .contact-avatar{width:32px;height:32px;border-radius:50%;background:var(--gradient-blue);display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700}
.phone-header .contact-info{flex:1}
.phone-header .contact-name{color:#fff;font-size:.85rem;font-weight:600}
.phone-header .contact-status{color:rgba(255,255,255,.7);font-size:.65rem}
.chat-body{flex:1;padding:12px;display:flex;flex-direction:column;gap:6px;overflow:hidden}
.msg{max-width:82%;padding:8px 12px;border-radius:10px;font-size:.78rem;line-height:1.4;position:relative}
.msg .time{font-size:.6rem;color:rgba(255,255,255,.45);float:right;margin:4px 0 0 10px}
.msg-in{background:#1f2c33;color:#e9edef;align-self:flex-start;border-top-left-radius:2px}
.msg-out{background:#005c4b;color:#e9edef;align-self:flex-end;border-top-right-radius:2px}
.msg-out .time{color:rgba(255,255,255,.5)}
.typing-indicator{align-self:flex-start;background:#1f2c33;padding:10px 16px;border-radius:10px;display:flex;gap:4px;align-items:center}
.typing-indicator span{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.4);animation:typingBounce 1.4s infinite}
.typing-indicator span:nth-child(2){animation-delay:.2s}
.typing-indicator span:nth-child(3){animation-delay:.4s}
@keyframes typingBounce{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-4px);opacity:1}}

/* Floating cards */
.float-card{
position:absolute;padding:12px 18px;border-radius:var(--radius-lg);
background:rgba(15,31,58,.9);backdrop-filter:blur(12px);
border:1px solid rgba(15,252,190,.15);
box-shadow:0 8px 32px rgba(0,0,0,.3);
animation:floatCard 4s ease-in-out infinite;
z-index:2;
}
.float-card.fc1{top:60px;right:-30px;animation-delay:0s}
.float-card.fc2{bottom:100px;left:-40px;animation-delay:1.5s}
@keyframes floatCard{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.float-card .fc-icon{font-size:1.2rem;margin-bottom:4px}
.float-card .fc-label{font-size:.7rem;color:var(--text-muted)}
.float-card .fc-value{font-size:.95rem;font-weight:700;color:var(--accent)}

/* ===== PROOF BAR ===== */
.proof-bar{
padding:32px 0;
border-top:1px solid var(--border-color);border-bottom:1px solid var(--border-color);
background:var(--bg-section);
}
.proof-inner{display:flex;align-items:center;justify-content:center;gap:40px;flex-wrap:wrap}
.proof-item{
font-family:'DM Sans',sans-serif;font-weight:700;font-size:.82rem;
color:var(--text-muted);letter-spacing:2px;text-transform:uppercase;
display:flex;align-items:center;gap:8px;
}
.proof-item::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--accent);opacity:.5}

/* ===== PROBLEMA ===== */
.problema{background:var(--bg-section)}
.pain-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-bottom:60px}
.pain-card{
padding:28px;border-radius:var(--radius-lg);
background:var(--bg-card);border:1px solid var(--border-color);
transition:all .3s;display:flex;gap:16px;align-items:flex-start;
}
.pain-card:hover{border-color:rgba(15,252,190,.2);transform:translateY(-2px)}
.pain-icon{font-size:1.5rem;flex-shrink:0;margin-top:2px}
.pain-card h4{font-size:1rem;margin-bottom:6px;font-weight:700}
.pain-card p{color:var(--text-secondary);font-size:.88rem}

.compare-table{width:100%;border-collapse:collapse;border-radius:var(--radius-lg);overflow:hidden}
.compare-table th{
padding:16px 24px;text-align:left;font-family:'DM Sans',sans-serif;font-weight:700;font-size:.95rem;
}
.compare-table th:first-child{background:transparent}
.compare-table th:nth-child(2){background:rgba(255,80,80,.1);color:#ff6b6b}
.compare-table th:nth-child(3){background:rgba(15,252,190,.08);color:var(--accent)}
.compare-table td{padding:14px 24px;font-size:.88rem;border-bottom:1px solid var(--border-color)}
.compare-table tr:last-child td{border-bottom:none}
.compare-table td:nth-child(2){color:#ff6b6b}
.compare-table td:nth-child(3){color:var(--accent);font-weight:600}
.compare-wrap{
background:var(--bg-card);border-radius:var(--radius-lg);overflow:hidden;
border:1px solid var(--border-color);
}

/* ===== SOLUCAO ===== */
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.feature-card{
padding:36px 28px;border-radius:var(--radius-lg);
background:var(--bg-card);border:1px solid var(--border-color);
transition:all .4s;position:relative;overflow:hidden;
}
.feature-card::before{
content:'';position:absolute;top:0;left:0;right:0;height:3px;
background:var(--gradient-blue);opacity:0;transition:opacity .3s;
}
.feature-card:hover{border-color:rgba(15,252,190,.25);transform:translateY(-4px);box-shadow:0 12px 40px rgba(15,252,190,.08)}
.feature-card:hover::before{opacity:1}
.feature-icon{
width:52px;height:52px;border-radius:var(--radius-sm);
background:rgba(15,252,190,.08);border:1px solid rgba(15,252,190,.15);
display:flex;align-items:center;justify-content:center;
font-size:1.4rem;margin-bottom:20px;
}
.feature-card h3{font-size:1.1rem;margin-bottom:10px;font-weight:700}
.feature-card p{color:var(--text-secondary);font-size:.88rem;line-height:1.6}

/* ===== STATS ===== */
.stats-section{
background:linear-gradient(135deg,rgba(16,110,190,.12),rgba(15,252,190,.06));
border-top:1px solid rgba(15,252,190,.1);border-bottom:1px solid rgba(15,252,190,.1);
padding:80px 0;
}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px;text-align:center}
.stat-item .stat-number{
font-family:'DM Sans',sans-serif;font-size:clamp(2rem,5vw,3.2rem);font-weight:800;
background:var(--gradient-blue);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.stat-item .stat-label{color:var(--text-secondary);font-size:.9rem;margin-top:4px}

/* ===== COMO FUNCIONA ===== */
.como-funciona{background:var(--bg-section)}
.steps-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;position:relative}
.steps-grid::before{
content:'';position:absolute;top:40px;left:12%;right:12%;height:2px;
background:linear-gradient(90deg,var(--primary),var(--accent));opacity:.2;
}
.step-card{text-align:center;position:relative;z-index:1}
.step-number{
width:64px;height:64px;border-radius:50%;margin:0 auto 20px;
background:var(--bg-card);border:2px solid var(--accent);
display:flex;align-items:center;justify-content:center;
font-family:'DM Sans',sans-serif;font-weight:800;font-size:1.2rem;color:var(--accent);
}
.step-card h3{font-size:1.05rem;margin-bottom:8px;font-weight:700}
.step-card p{color:var(--text-secondary);font-size:.85rem}

/* ===== SETORES ===== */
.sectors-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.sector-card{
padding:28px 20px;border-radius:var(--radius-lg);
background:var(--bg-card);border:1px solid var(--border-color);
text-align:center;transition:all .3s;
}
.sector-card:hover{border-color:rgba(15,252,190,.25);transform:translateY(-3px);box-shadow:0 8px 30px rgba(15,252,190,.06)}
.sector-emoji{font-size:2.2rem;margin-bottom:12px;display:block}
.sector-card h4{font-size:.95rem;font-weight:700}

/* ===== RESULTADOS ===== */
.resultados{background:var(--bg-section)}
.testimonials-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.testimonial-card{
padding:32px;border-radius:var(--radius-lg);
background:var(--bg-card);border:1px solid var(--border-color);
transition:all .3s;position:relative;
}
.testimonial-card:hover{border-color:rgba(15,252,190,.2);transform:translateY(-3px)}
.testimonial-stars{color:var(--accent);font-size:.9rem;margin-bottom:16px;letter-spacing:2px}
.testimonial-card blockquote{color:var(--text-secondary);font-size:.92rem;line-height:1.7;margin-bottom:20px;font-style:italic}
.testimonial-author{display:flex;align-items:center;gap:12px}
.testimonial-avatar{
width:44px;height:44px;border-radius:50%;
background:var(--gradient-blue);display:flex;align-items:center;justify-content:center;
font-weight:700;font-size:.85rem;color:#0a1628;
}
.testimonial-info .t-name{font-weight:700;font-size:.9rem}
.testimonial-info .t-role{color:var(--text-muted);font-size:.78rem}

/* ===== GARANTIA ===== */
.garantia-box{
max-width:800px;margin:0 auto;padding:48px;border-radius:var(--radius-lg);
background:var(--bg-card);border:1px solid rgba(15,252,190,.15);
text-align:center;position:relative;overflow:hidden;
}
.garantia-box::before{
content:'';position:absolute;top:0;left:0;right:0;height:3px;
background:var(--gradient-blue);
}
.garantia-shield{font-size:3.5rem;margin-bottom:16px;display:block}
.garantia-box h2{font-size:1.8rem;margin-bottom:12px}
.garantia-box>p{color:var(--text-secondary);margin-bottom:28px}
.garantia-points{list-style:none;display:flex;flex-direction:column;gap:12px;text-align:left;max-width:500px;margin:0 auto}
.garantia-points li{display:flex;align-items:center;gap:12px;color:var(--text-secondary);font-size:.92rem}
.garantia-points li .check{color:var(--accent);font-weight:700;font-size:1.1rem}

/* ===== FAQ ===== */
.faq-section{background:var(--bg-section)}
.faq-list{max-width:780px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
.faq-item{
border-radius:var(--radius-lg);overflow:hidden;
background:var(--bg-card);border:1px solid var(--border-color);
transition:border-color .3s;
}
.faq-item[open]{border-color:rgba(15,252,190,.2)}
.faq-item summary{
padding:20px 24px;cursor:pointer;font-family:'DM Sans',sans-serif;
font-weight:700;font-size:1rem;display:flex;align-items:center;
justify-content:space-between;list-style:none;transition:color .3s;
}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:'+';font-size:1.4rem;color:var(--accent);transition:transform .3s}
.faq-item[open] summary::after{content:'-'}
.faq-item summary:hover{color:var(--accent)}
.faq-answer{padding:0 24px 20px;color:var(--text-secondary);font-size:.9rem;line-height:1.7}

/* ===== CTA FINAL ===== */
.cta-final{
text-align:center;
background:linear-gradient(180deg,var(--bg-dark) 0%,rgba(16,110,190,.1) 50%,var(--bg-dark) 100%);
position:relative;
}
.cta-final h2{font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:16px}
.cta-final .cta-sub{color:var(--text-secondary);font-size:1.05rem;margin-bottom:36px;max-width:560px;margin-left:auto;margin-right:auto}
.cta-urgency{
display:inline-flex;align-items:center;gap:8px;
padding:10px 20px;border-radius:var(--radius-pill);
background:rgba(15,252,190,.06);border:1px solid rgba(15,252,190,.15);
color:var(--accent);font-size:.82rem;font-weight:600;margin-top:24px;
}

/* ===== FOOTER ===== */
footer{
padding:48px 0 24px;border-top:1px solid var(--border-color);
background:var(--bg-dark);
}
.footer-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px;margin-bottom:40px}
.footer-brand .nav-logo{margin-bottom:12px}
.footer-brand p{color:var(--text-muted);font-size:.85rem;max-width:280px}
.footer-col h4{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.95rem;margin-bottom:16px;color:var(--accent)}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col ul li a{color:var(--text-muted);font-size:.85rem;transition:color .3s}
.footer-col ul li a:hover{color:var(--accent)}
.footer-bottom{
border-top:1px solid var(--border-color);padding-top:24px;
display:flex;align-items:center;justify-content:space-between;
color:var(--text-muted);font-size:.8rem;
}

/* ===== WA FLOAT ===== */
.wa-float{
position:fixed;bottom:28px;right:28px;z-index:999;
width:60px;height:60px;border-radius:50%;
background:#25d366;display:flex;align-items:center;justify-content:center;
box-shadow:0 6px 24px rgba(37,211,102,.4);
transition:all .3s;animation:waFloat 3s ease-in-out infinite;
}
.wa-float:hover{transform:scale(1.1);box-shadow:0 8px 32px rgba(37,211,102,.5)}
@keyframes waFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.wa-float svg{width:30px;height:30px;fill:#fff}

/* ===== RESPONSIVE ===== */
@media(max-width:1024px){
.hero-grid{grid-template-columns:1fr;text-align:center}
.hero-sub{margin-left:auto;margin-right:auto}
.hero-buttons{justify-content:center}
.hero-social-proof{justify-content:center}
.phone-wrapper{margin-top:40px}
.float-card.fc1{right:0}
.float-card.fc2{left:10px}
.features-grid{grid-template-columns:repeat(2,1fr)}
.stats-grid{grid-template-columns:repeat(2,1fr);gap:40px}
.steps-grid{grid-template-columns:repeat(2,1fr)}
.steps-grid::before{display:none}
.sectors-grid{grid-template-columns:repeat(2,1fr)}
.testimonials-grid{grid-template-columns:1fr}
.footer-grid{grid-template-columns:1fr}
}
@media(max-width:768px){
.nav-links{display:none}
.hamburger{display:flex}
.hero{padding:120px 0 60px}
.pain-grid{grid-template-columns:1fr}
.features-grid{grid-template-columns:1fr}
.stats-grid{grid-template-columns:repeat(2,1fr)}
.steps-grid{grid-template-columns:1fr}
.sectors-grid{grid-template-columns:repeat(2,1fr)}
.proof-inner{gap:20px}
.proof-item{font-size:.7rem}
.compare-table th,.compare-table td{padding:10px 12px;font-size:.78rem}
.garantia-box{padding:32px 20px}
.footer-bottom{flex-direction:column;gap:12px;text-align:center}
section{padding:70px 0}
}
</style>
</head>
<body>

<!-- NAV -->
<nav class="navbar" id="navbar">
<div class="container nav-inner">
<a href="#" class="nav-logo">
<div class="logo-icon">O</div>
OAKEN IA
</a>
<ul class="nav-links">
<li><a href="#solucao">O que faz</a></li>
<li><a href="#como-funciona">Como funciona</a></li>
<li><a href="#resultados">Resultados</a></li>
<li><a href="#faq">FAQ</a></li>
<li><a href="https://wa.me/351913388794" target="_blank" class="nav-cta">Falar com especialista</a></li>
</ul>
<button class="hamburger" onclick="document.getElementById('mobileMenu').classList.add('active')" aria-label="Menu">
<span></span><span></span><span></span>
</button>
</div>
</nav>

<!-- MOBILE MENU -->
<div class="mobile-menu" id="mobileMenu">
<button class="mobile-close" onclick="this.parentElement.classList.remove('active')">&times;</button>
<a href="#solucao" onclick="this.parentElement.classList.remove('active')">O que faz</a>
<a href="#como-funciona" onclick="this.parentElement.classList.remove('active')">Como funciona</a>
<a href="#resultados" onclick="this.parentElement.classList.remove('active')">Resultados</a>
<a href="#faq" onclick="this.parentElement.classList.remove('active')">FAQ</a>
<a href="https://wa.me/351913388794" target="_blank" class="btn-primary">Falar com especialista</a>
</div>

<!-- HERO -->
<section class="hero">
<div class="deco-circle c1"></div>
<div class="deco-circle c2"></div>
<div class="container">
<div class="hero-grid">
<div class="reveal">
<div class="hero-badge">
<span class="pulse"></span>
Agente de IA para WhatsApp
</div>
<h1>
Seu negocio <span class="highlight">atendendo e vendendo</span> enquanto voce descansa
</h1>
<p class="hero-sub">
Um agente inteligente que responde, qualifica e converte seus clientes no WhatsApp automaticamente, 24 horas por dia.
</p>
<div class="hero-buttons">
<a href="https://wa.me/351913388794" target="_blank" class="btn-primary">
<svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.116.553 4.1 1.519 5.823L.525 23.393a.5.5 0 0 0 .612.612l5.57-.994A11.944 11.944 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.282-1.51l-.376-.226-3.307.59.59-3.307-.226-.376A9.94 9.94 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
Quero meu agente IA
</a>
<a href="#como-funciona" class="btn-outline">Como funciona</a>
</div>
<div class="hero-social-proof">
<div class="avatar-stack">
<div class="av">C</div>
<div class="av">R</div>
<div class="av">A</div>
<div class="av">M</div>
</div>
<div class="social-text"><strong>+120 negocios</strong> ja usam</div>
</div>
</div>
<div class="phone-wrapper reveal">
<div class="phone-mockup">
<div class="phone-screen">
<div class="phone-header">
<span class="back-arrow">&larr;</span>
<div class="contact-avatar">O</div>
<div class="contact-info">
<div class="contact-name">Oaken IA</div>
<div class="contact-status">online</div>
</div>
</div>
<div class="chat-body">
<div class="msg msg-in">
Ola! Vi voces no Instagram. Voces atendem no centro?
<span class="time">10:30</span>
</div>
<div class="msg msg-out">
Oi! Sim, atendemos! Temos unidades no centro e zona sul. Posso ja verificar um horario para voce?
<span class="time">10:30</span>
</div>
<div class="msg msg-in">
Sim! Quero para amanha a tarde
<span class="time">10:31</span>
</div>
<div class="msg msg-out">
Perfeito! Temos disponivel: Amanha as 14h ou 16h30. Qual prefere?
<span class="time">10:31</span>
</div>
<div class="msg msg-in">
14h ta otimo!
<span class="time">10:32</span>
</div>
<div class="typing-indicator">
<span></span><span></span><span></span>
</div>
</div>
</div>
</div>
<div class="float-card fc1">
<div class="fc-icon">&#9889;</div>
<div class="fc-label">Tempo de resposta</div>
<div class="fc-value">&lt; 3 segundos</div>
</div>
<div class="float-card fc2">
<div class="fc-icon">&#128200;</div>
<div class="fc-label">Taxa de conversao</div>
<div class="fc-value">+40% vendas</div>
</div>
</div>
</div>
</div>
</section>

<!-- PROOF BAR -->
<div class="proof-bar">
<div class="container">
<div class="proof-inner">
<div class="proof-item">Clinica Medica</div>
<div class="proof-item">Imobiliaria</div>
<div class="proof-item">Academia</div>
<div class="proof-item">Restaurante</div>
<div class="proof-item">Salao de Beleza</div>
<div class="proof-item">E-commerce</div>
</div>
</div>
</div>

<!-- PROBLEMA -->
<section class="problema" id="problema">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">O Problema</div>
<h2 class="section-title">Cada mensagem sem resposta e <span class="gradient-text">dinheiro perdido</span></h2>
<p class="section-sub">Enquanto voce dorme, seus concorrentes respondem. Enquanto voce almoca, clientes vao embora.</p>
</div>
<div class="pain-grid reveal">
<div class="pain-card">
<div class="pain-icon">&#128556;</div>
<div>
<h4>Clientes ignorados</h4>
<p>78% dos clientes compram de quem responde primeiro. Mensagens sem resposta sao vendas perdidas.</p>
</div>
</div>
<div class="pain-card">
<div class="pain-icon">&#128564;</div>
<div>
<h4>Sem atendimento fora do horario</h4>
<p>Seu negocio fecha as 18h, mas seus clientes pesquisam ate a meia-noite. Quem responde?</p>
</div>
</div>
<div class="pain-card">
<div class="pain-icon">&#128176;</div>
<div>
<h4>Equipe cara e limitada</h4>
<p>Contratar atendentes custa caro e nao escala. Treinar leva tempo. Turnover e alto.</p>
</div>
</div>
<div class="pain-card">
<div class="pain-icon">&#128200;</div>
<div>
<h4>Zero dados e insights</h4>
<p>Voce nao sabe quantos leads perdeu, quais perguntas sao mais frequentes, ou onde o funil quebra.</p>
</div>
</div>
</div>
<div class="compare-wrap reveal">
<table class="compare-table">
<thead>
<tr>
<th></th>
<th>&#10060; Sem IA</th>
<th>&#10004; Com Oaken IA</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tempo de resposta</td>
<td>30 min a 2 horas</td>
<td>Menos de 3 segundos</td>
</tr>
<tr>
<td>Horario de atendimento</td>
<td>Horario comercial</td>
<td>24h por dia, 7 dias</td>
</tr>
<tr>
<td>Capacidade</td>
<td>1 conversa por vez</td>
<td>Ilimitadas simultaneas</td>
</tr>
<tr>
<td>Custo mensal</td>
<td>R$ 3.000+ por atendente</td>
<td>Fracao do custo</td>
</tr>
<tr>
<td>Qualidade</td>
<td>Varia com humor e cansaco</td>
<td>Consistente e otimizada</td>
</tr>
</tbody>
</table>
</div>
</div>
</section>

<!-- SOLUCAO -->
<section id="solucao">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">Solucao</div>
<h2 class="section-title">Tudo que seu negocio precisa, <span class="gradient-text">num so agente</span></h2>
<p class="section-sub">Nosso agente de IA faz o trabalho de uma equipe inteira, com qualidade superior e custo muito menor.</p>
</div>
<div class="features-grid reveal">
<div class="feature-card">
<div class="feature-icon">&#129302;</div>
<h3>Atendimento Inteligente</h3>
<p>Respostas naturais e contextuais que entendem o que o cliente realmente quer, sem parecer um robo.</p>
</div>
<div class="feature-card">
<div class="feature-icon">&#128197;</div>
<h3>Agendamento Automatico</h3>
<p>Agenda consultas, reunioes e servicos diretamente pelo WhatsApp, integrado ao seu calendario.</p>
</div>
<div class="feature-card">
<div class="feature-icon">&#128176;</div>
<h3>Vendas no Chat</h3>
<p>Qualifica leads, apresenta produtos e guia o cliente ate a compra sem intervencao humana.</p>
</div>
<div class="feature-card">
<div class="feature-icon">&#128232;</div>
<h3>Follow-up Automatico</h3>
<p>Nunca mais perca uma venda por esquecimento. O agente faz follow-up no momento certo.</p>
</div>
<div class="feature-card">
<div class="feature-icon">&#128202;</div>
<h3>Relatorios e Insights</h3>
<p>Dashboard completo com metricas de atendimento, satisfacao e oportunidades de melhoria.</p>
</div>
<div class="feature-card">
<div class="feature-icon">&#128268;</div>
<h3>Integracao Completa</h3>
<p>Conecta com seu CRM, Google Calendar, planilhas e ferramentas que voce ja usa.</p>
</div>
</div>
</div>
</section>

<!-- STATS -->
<section class="stats-section">
<div class="container">
<div class="stats-grid reveal">
<div class="stat-item">
<div class="stat-number" data-target="98" data-suffix="%">0%</div>
<div class="stat-label">Satisfacao dos clientes</div>
</div>
<div class="stat-item">
<div class="stat-number" data-target="3" data-suffix="x">0x</div>
<div class="stat-label">Mais conversoes em vendas</div>
</div>
<div class="stat-item">
<div class="stat-number" data-target="24" data-suffix="h">0h</div>
<div class="stat-label">Disponivel sem parar</div>
</div>
<div class="stat-item">
<div class="stat-number" data-target="7" data-suffix=" dias">0 dias</div>
<div class="stat-label">Para estar no ar</div>
</div>
</div>
</div>
</section>

<!-- COMO FUNCIONA -->
<section class="como-funciona" id="como-funciona">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">Processo</div>
<h2 class="section-title">Do zero ao <span class="gradient-text">agente no ar</span> em 7 dias</h2>
<p class="section-sub">Um processo simples e acompanhado para voce ter seu agente funcionando rapidamente.</p>
</div>
<div class="steps-grid reveal">
<div class="step-card">
<div class="step-number">1</div>
<h3>Diagnostico</h3>
<p>Analisamos seu negocio, fluxo de atendimento e objetivos para criar a estrategia ideal.</p>
</div>
<div class="step-card">
<div class="step-number">2</div>
<h3>Configuracao</h3>
<p>Construimos e treinamos seu agente com a personalidade, tom e conhecimento do seu negocio.</p>
</div>
<div class="step-card">
<div class="step-number">3</div>
<h3>Testes</h3>
<p>Rodamos testes rigorosos para garantir que o agente responde com qualidade e precisao.</p>
</div>
<div class="step-card">
<div class="step-number">4</div>
<h3>No Ar</h3>
<p>Seu agente entra em acao e voce acompanha os resultados em tempo real pelo dashboard.</p>
</div>
</div>
</div>
</section>

<!-- SETORES -->
<section id="setores">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">Setores</div>
<h2 class="section-title">Feito para <span class="gradient-text">diversos setores</span></h2>
<p class="section-sub">Nosso agente se adapta as necessidades especificas de cada tipo de negocio.</p>
</div>
<div class="sectors-grid reveal">
<div class="sector-card">
<span class="sector-emoji">&#127973;</span>
<h4>Clinicas e Saude</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#127968;</span>
<h4>Imobiliarias</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#128170;</span>
<h4>Academias e Studios</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#127860;</span>
<h4>Restaurantes</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#128135;</span>
<h4>Saloes de Beleza</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#128722;</span>
<h4>E-commerce</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#127891;</span>
<h4>Escolas e Cursos</h4>
</div>
<div class="sector-card">
<span class="sector-emoji">&#9878;&#65039;</span>
<h4>Escritorios e Servicos</h4>
</div>
</div>
</div>
</section>

<!-- RESULTADOS -->
<section class="resultados" id="resultados">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">Resultados</div>
<h2 class="section-title">Quem usa, <span class="gradient-text">recomenda</span></h2>
<p class="section-sub">Veja o que nossos clientes dizem sobre a experiencia com a Oaken IA.</p>
</div>
<div class="testimonials-grid reveal">
<div class="testimonial-card">
<div class="testimonial-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
<blockquote>"Minha clinica triplicou os agendamentos no primeiro mes. O agente responde melhor que minha antiga recepcionista e nunca falta ao trabalho."</blockquote>
<div class="testimonial-author">
<div class="testimonial-avatar">C</div>
<div class="testimonial-info">
<div class="t-name">Carolina M.</div>
<div class="t-role">Clinica de Estetica - Sao Paulo</div>
</div>
</div>
</div>
<div class="testimonial-card">
<div class="testimonial-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
<blockquote>"Antes eu perdia leads no fim de semana. Agora o agente agenda visitas 24h e minha taxa de conversao subiu 40%. Retorno do investimento em 2 semanas."</blockquote>
<div class="testimonial-author">
<div class="testimonial-avatar">R</div>
<div class="testimonial-info">
<div class="t-name">Roberto S.</div>
<div class="t-role">Imobiliaria - Porto</div>
</div>
</div>
</div>
<div class="testimonial-card">
<div class="testimonial-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
<blockquote>"Tenho 3 studios de pilates e o agente gerencia agendamentos de todos. Reduzi custos com atendimento em 60% e meus alunos adoram a rapidez."</blockquote>
<div class="testimonial-author">
<div class="testimonial-avatar">A</div>
<div class="testimonial-info">
<div class="t-name">Amanda L.</div>
<div class="t-role">Studios de Pilates - Lisboa</div>
</div>
</div>
</div>
</div>
</div>
</section>

<!-- GARANTIA -->
<section id="garantia">
<div class="container">
<div class="garantia-box reveal">
<span class="garantia-shield">&#128737;&#65039;</span>
<h2>Garantia de <span class="gradient-text">30 dias</span></h2>
<p>Se nos primeiros 30 dias voce nao ver resultados reais, devolvemos 100% do seu investimento.</p>
<ul class="garantia-points">
<li><span class="check">&#10003;</span> Sem risco para voce</li>
<li><span class="check">&#10003;</span> Sem burocracia para cancelar</li>
<li><span class="check">&#10003;</span> Sem perguntas — devolucao total</li>
<li><span class="check">&#10003;</span> Suporte dedicado durante todo o periodo</li>
</ul>
</div>
</div>
</section>

<!-- FAQ -->
<section class="faq-section" id="faq">
<div class="container">
<div style="text-align:center" class="reveal">
<div class="section-label">FAQ</div>
<h2 class="section-title">Perguntas <span class="gradient-text">frequentes</span></h2>
<p class="section-sub">Tire suas duvidas sobre como a Oaken IA pode transformar seu atendimento.</p>
</div>
<div class="faq-list reveal">
<details class="faq-item">
<summary>Preciso ter conhecimento tecnico para usar?</summary>
<div class="faq-answer">Nao! Nos cuidamos de toda a configuracao e treinamento do agente. Voce so precisa nos contar sobre seu negocio e nos fazemos o resto. A interface de acompanhamento e simples e intuitiva.</div>
</details>
<details class="faq-item">
<summary>O agente consegue entender perguntas complexas?</summary>
<div class="faq-answer">Sim. Nosso agente usa inteligencia artificial avancada que entende contexto, intencao e nuances. Ele aprende com seu negocio e melhora continuamente com base nas interacoes reais.</div>
</details>
<details class="faq-item">
<summary>E se o cliente quiser falar com um humano?</summary>
<div class="faq-answer">O agente identifica automaticamente quando deve transferir para um atendente humano. Voce define as regras de escalamento e o agente as segue rigorosamente.</div>
</details>
<details class="faq-item">
<summary>Funciona com meu numero de WhatsApp atual?</summary>
<div class="faq-answer">Sim! Integramos diretamente com a API oficial do WhatsApp Business. Voce mantem seu numero e seus clientes nem percebem que estao falando com IA.</div>
</details>
<details class="faq-item">
<summary>Quanto tempo leva para implementar?</summary>
<div class="faq-answer">Em media, 7 dias uteis. Isso inclui diagnostico, configuracao, treinamento do agente com suas informacoes e fase de testes antes de ir ao ar.</div>
</details>
<details class="faq-item">
<summary>Qual o investimento mensal?</summary>
<div class="faq-answer">Temos planos a partir de valores acessiveis que se pagam rapidamente. O retorno medio dos nossos clientes e de 5x o investimento no primeiro mes. Fale com um especialista para uma proposta personalizada.</div>
</details>
</div>
</div>
</section>

<!-- CTA FINAL -->
<section class="cta-final">
<div class="container reveal">
<div class="section-label">Comece Agora</div>
<h2 class="section-title">Comece a atender e vender<br><span class="gradient-text">enquanto dorme</span></h2>
<p class="cta-sub">Junte-se a mais de 120 negocios que ja transformaram seu atendimento com inteligencia artificial.</p>
<a href="https://wa.me/351913388794" target="_blank" class="btn-primary" style="font-size:1.05rem;padding:18px 40px">
<svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.116.553 4.1 1.519 5.823L.525 23.393a.5.5 0 0 0 .612.612l5.57-.994A11.944 11.944 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.282-1.51l-.376-.226-3.307.59.59-3.307-.226-.376A9.94 9.94 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
Falar com especialista agora
</a>
<div class="cta-urgency">
&#9889; Vagas limitadas para este mes — Garanta a sua
</div>
</div>
</section>

<!-- FOOTER -->
<footer>
<div class="container">
<div class="footer-grid">
<div class="footer-brand">
<div class="nav-logo">
<div class="logo-icon">O</div>
OAKEN IA
</div>
<p>Agentes de inteligencia artificial para WhatsApp que atendem, agendam e vendem para o seu negocio.</p>
</div>
<div class="footer-col">
<h4>Links</h4>
<ul>
<li><a href="#solucao">O que faz</a></li>
<li><a href="#como-funciona">Como funciona</a></li>
<li><a href="#resultados">Resultados</a></li>
<li><a href="#faq">FAQ</a></li>
</ul>
</div>
<div class="footer-col">
<h4>Contato</h4>
<ul>
<li><a href="https://wa.me/351913388794" target="_blank">WhatsApp: +351 913 388 794</a></li>
<li><a href="#">contato@oakenia.com</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<span>&copy; 2026 Oaken IA. Todos os direitos reservados.</span>
<span>Feito com &#128154; e inteligencia artificial</span>
</div>
</div>
</footer>

<!-- WA FLOAT -->
<a href="https://wa.me/351913388794" target="_blank" class="wa-float" aria-label="WhatsApp">
<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.116.553 4.1 1.519 5.823L.525 23.393a.5.5 0 0 0 .612.612l5.57-.994A11.944 11.944 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.94 9.94 0 0 1-5.282-1.51l-.376-.226-3.307.59.59-3.307-.226-.376A9.94 9.94 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
</a>

<script>
// Navbar scroll
const navbar=document.getElementById('navbar');
window.addEventListener('scroll',()=>{navbar.classList.toggle('scrolled',window.scrollY>50)});

// Reveal on scroll
const revealEls=document.querySelectorAll('.reveal');
const revealObs=new IntersectionObserver((entries)=>{
entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');revealObs.unobserve(e.target)}})
},{threshold:0.15});
revealEls.forEach(el=>revealObs.observe(el));

// Counter animation
function animateCounter(el){
const target=parseInt(el.dataset.target);
const suffix=el.dataset.suffix||'';
const duration=2000;
const start=performance.now();
function update(now){
const elapsed=now-start;
const progress=Math.min(elapsed/duration,1);
const eased=1-Math.pow(1-progress,3);
const current=Math.round(eased*target);
el.textContent=current+suffix;
if(progress<1)requestAnimationFrame(update);
}
requestAnimationFrame(update);
}
const statEls=document.querySelectorAll('.stat-number[data-target]');
const statsObs=new IntersectionObserver((entries)=>{
entries.forEach(e=>{if(e.isIntersecting){animateCounter(e.target);statsObs.unobserve(e.target)}})
},{threshold:0.5});
statEls.forEach(el=>statsObs.observe(el));

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a=>{
a.addEventListener('click',e=>{
const t=document.querySelector(a.getAttribute('href'));
if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'})}
});
});
</script>
</body>
</html>
