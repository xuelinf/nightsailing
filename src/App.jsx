import React, { useEffect, useMemo, useState } from "react";
import { products, siteMeta } from "./products.js";
import heroImage from "./assets/night-voyage-hero.png";

function getInitialSlug() {
  return window.location.hash.replace(/^#\/product\//, "") || "";
}

function App() {
  const [activeSlug, setActiveSlug] = useState(getInitialSlug);
  const activeProduct = useMemo(
    () => products.find((product) => product.slug === activeSlug),
    [activeSlug],
  );

  useEffect(() => {
    const handleHashChange = () => setActiveSlug(getInitialSlug());
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  function openProduct(slug) {
    window.location.hash = `/product/${slug}`;
    setActiveSlug(slug);
  }

  function goHome() {
    window.location.hash = "";
    setActiveSlug("");
  }

  return (
    <main className="site-shell">
      <Nav onHome={goHome} />
      {activeProduct ? (
        <ProductDetail product={activeProduct} onHome={goHome} />
      ) : (
        <Home onOpenProduct={openProduct} />
      )}
    </main>
  );
}

function Nav({ onHome }) {
  return (
    <header className="site-nav">
      <nav className="nav-links" aria-label="主导航">
        <button onClick={onHome}>工具</button>
        <a href="#log">日志</a>
      </nav>
      <button className="brand-mark" onClick={onHome} aria-label="回到首页">
        {siteMeta.name}
      </button>
      <div className="nav-actions">
        <a href={siteMeta.githubHref} target="_blank" rel="noreferrer">GitHub</a>
        <a className="filled-link" href="#catalog">下载最新</a>
      </div>
    </header>
  );
}

function Home({ onOpenProduct }) {
  return (
    <>
      <section className="hero-section">
        <img className="hero-image" src={heroImage} alt="" />
        <div className="hero-copy">
          <p className="micro-label">AI TOOLS / VERSION 0.0.1</p>
          <h1>夜航船之书</h1>
          <p className="hero-text">把自己做过、用过、还在打磨的 AI 工具收进一艘船。这里先放能下载的作品，也给将要做的工具留出舱位。</p>
          <div className="hero-actions">
            <a className="primary-action" href="#catalog">查看工具</a>
            <a className="ghost-action" href="#log">阅读航行日志</a>
          </div>
        </div>
      </section>

      <section className="catalog-section" id="catalog">
        <div className="section-heading">
          <div>
            <p className="micro-label">CATALOG</p>
            <h2>船舱目录</h2>
          </div>
          <p>每张卡片回答三件事：它解决什么问题、现在能不能下载、源码是否开放。</p>
        </div>
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.slug} product={product} onOpen={() => onOpenProduct(product.slug)} />
          ))}
        </div>
      </section>

      <section className="story-section">
        <p className="micro-label">WHY NIGHT SAILING</p>
        <h2>不是把工具摆上货架，而是把有用之物收入船舱。</h2>
        <p>“夜航船”在这里不是复古装饰，而是一种工作方式：在无人催促的夜里继续试、继续造，把真正能帮到自己的东西留下。这个网站先承担目录、下载和开源索引，后面会慢慢长成一册开发日志。</p>
      </section>

      <section className="log-section" id="log">
        <div className="section-heading compact">
          <div>
            <p className="micro-label">LOGBOOK</p>
            <h2>航行日志</h2>
          </div>
          <p>0.0.1 先建立站点、目录和下载入口。</p>
        </div>
        <div className="log-list">
          <article><span>0.0.1</span><p>建立“夜航船之书”首页、四个产品位和两个 macOS 工具下载入口。</p></article>
          <article><span>next</span><p>为端口占用管理器与 AI 语音输入补充原型、源码入口和发布说明。</p></article>
        </div>
      </section>

      <Footer />
    </>
  );
}

function ProductCard({ product, onOpen }) {
  const isAvailable = product.status === "available";
  return (
    <article className={`product-card ${isAvailable ? "is-available" : "is-planned"}`}>
      <div>
        <div className="tag-row">
          <span>{product.statusLabel}</span>
          <span>{product.openSourceLabel}</span>
        </div>
        <h3>{product.name}</h3>
        <p>{product.summary}</p>
      </div>
      <div className="card-actions">
        <button className={isAvailable ? "primary-action small" : "ghost-action small"} onClick={onOpen}>
          {isAvailable ? "进入" : "查看计划"}
        </button>
        {product.sourceHref ? <a className="ghost-action small" href={product.sourceHref} target="_blank" rel="noreferrer">源码</a> : null}
      </div>
    </article>
  );
}

function ProductDetail({ product, onHome }) {
  const isAvailable = product.status === "available";
  return (
    <section className="detail-section">
      <button className="back-button" onClick={onHome}>返回船舱目录</button>
      <article className="detail-panel">
        <div className="detail-kicker">
          <span>{product.platform}</span>
          <span>{product.statusLabel}</span>
          <span>{product.openSourceLabel}</span>
        </div>
        <h1>{product.name}</h1>
        <p className="detail-summary">{product.detail}</p>
        <div className="detail-actions">
          {product.downloadHref ? <a className="primary-action" href={product.downloadHref}>下载 DMG</a> : <span className="disabled-action">预留舱位</span>}
          {product.sourceHref ? <a className="ghost-action" href={product.sourceHref} target="_blank" rel="noreferrer">查看源码</a> : null}
        </div>
        <div className="detail-grid">
          <section>
            <p className="micro-label">FEATURES</p>
            <ul>
              {product.features.map((feature) => <li key={feature}>{feature}</li>)}
            </ul>
          </section>
          <section>
            <p className="micro-label">PRIVACY</p>
            <p>{product.privacy}</p>
            {!isAvailable ? <p className="planned-note">这个产品还在计划中，首版网站不会伪造下载入口。</p> : null}
          </section>
        </div>
      </article>
    </section>
  );
}

function Footer() {
  return (
    <footer className="site-footer">
      <span>夜航船之书 · 0.0.1</span>
      <a href={siteMeta.githubHref} target="_blank" rel="noreferrer">xuelinf/nightsailing</a>
    </footer>
  );
}

export default App;
