import React, { useEffect, useMemo, useState } from "react";
import { products, siteMeta } from "./products.js";
import heroImage from "./assets/night-voyage-hero.png";
import aiSailingLogImage from "./assets/products/ai-sailing-log.png";
import wenxuanImage from "./assets/products/wenxuan.png";
import portKeeperImage from "./assets/products/port-keeper.png";
import aiVoiceInputImage from "./assets/products/ai-voice-input.png";

const productImages = {
  "ai-sailing-log": aiSailingLogImage,
  wenxuan: wenxuanImage,
  "port-keeper": portKeeperImage,
  "ai-voice-input": aiVoiceInputImage,
};

function getInitialSlug() {
  const match = window.location.hash.match(/^#\/product\/(.+)$/);
  return match ? decodeURIComponent(match[1]) : "";
}

function App() {
  const [activeSlug, setActiveSlug] = useState(getInitialSlug);
  const activeProduct = useMemo(
    () => products.find((product) => product.slug === activeSlug),
    [activeSlug],
  );

  useEffect(() => {
    const handleHashChange = () => {
      const nextSlug = getInitialSlug();
      setActiveSlug(nextSlug);
      if (nextSlug) {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    };
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  function openProduct(slug) {
    window.location.hash = `/product/${slug}`;
    setActiveSlug(slug);
  }

  function goHome(targetId = "") {
    setActiveSlug("");
    window.location.hash = targetId ? `#${targetId}` : "";
    if (targetId) {
      window.setTimeout(() => {
        document.getElementById(targetId)?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 0);
      return;
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
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
      <button className="brand-mark" onClick={() => onHome()} aria-label="回到首页">
        {siteMeta.name}
      </button>
      <nav className="nav-links" aria-label="主导航">
        <button onClick={() => onHome("catalog")}>工具</button>
        <button onClick={() => onHome("maintenance")}>维护</button>
        <a href={siteMeta.githubHref} target="_blank" rel="noreferrer">GitHub</a>
      </nav>
    </header>
  );
}

function Home({ onOpenProduct }) {
  const availableCount = products.filter((product) => product.status === "available").length;
  const openSourceCount = products.filter((product) => product.sourceHref || product.openSourceLabel.includes("开源")).length;

  return (
    <>
      <section className="hero-section" id="preface">
        <img className="hero-image" src={heroImage} alt="" />
        <div className="hero-shade" />
        <div className="hero-inner">
          <p className="micro-label">{siteMeta.edition}</p>
          <h1>{siteMeta.name}</h1>
          <p className="hero-line">{siteMeta.headline}</p>
          <p className="hero-text">{siteMeta.description}</p>
          <div className="hero-actions">
            <a className="primary-action" href="#catalog">{siteMeta.primaryCta}</a>
            <a className="ghost-action" href="#maintenance">{siteMeta.secondaryCta}</a>
          </div>
        </div>
        <dl className="hero-stats" aria-label="工具状态">
          <div><dt>{products.length}</dt><dd>工具条目</dd></div>
          <div><dt>{availableCount}</dt><dd>可下载</dd></div>
          <div><dt>{openSourceCount}</dt><dd>开源/计划开源</dd></div>
        </dl>
      </section>

      <section className="catalog-section" id="catalog">
        <div className="section-heading">
          <p className="micro-label">TOOLS</p>
          <h2>先看状态，再打开工具。</h2>
          <p>每个工具只保留判断所需的信息：用途、状态、平台、下载和源码。更完整的截图和视频，会在产品页逐步补齐。</p>
        </div>
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.slug} product={product} onOpen={() => onOpenProduct(product.slug)} />
          ))}
        </div>
      </section>

      <section className="maintenance-section" id="maintenance">
        <div>
          <p className="micro-label">MAINTENANCE</p>
          <h2>新产品先补资料，再上船。</h2>
        </div>
        <p>
          页面内容已经集中到 <code>content/site-content.md</code>。以后新增工具时，
          先在里面补产品名、一句话定位、三条能力、三条场景、下载/源码、真实素材和隐私边界，
          再进入页面实现。
        </p>
      </section>

      <Footer />
    </>
  );
}

function ProductCard({ product, onOpen }) {
  const isAvailable = product.status === "available";

  return (
    <article className={`product-card ${isAvailable ? "is-available" : "is-planned"}`}>
      <button className="card-open" onClick={onOpen}>
        <span className="card-image">
          <img src={productImages[product.slug]} alt="" />
        </span>
        <span className="card-body">
          <span className="card-meta">
            <em>{product.index}</em>
            <em>{product.statusLabel}</em>
            <em>{product.openSourceLabel}</em>
          </span>
          <strong>{product.name}</strong>
          <small>{product.category} · {product.platform}</small>
          <span>{product.summary}</span>
        </span>
      </button>
      <ul className="card-points">
        {product.highlights.slice(0, 3).map((item) => <li key={item}>{item}</li>)}
      </ul>
      <div className="card-actions">
        {product.downloadHref ? <a className="primary-action compact" href={product.downloadHref}>下载</a> : <span className="disabled-action compact">未发布</span>}
        {product.sourceHref ? <a className="ghost-action compact" href={product.sourceHref} target="_blank" rel="noreferrer">源码</a> : null}
        <button className="ghost-action compact" onClick={onOpen}>详情</button>
      </div>
    </article>
  );
}

function ProductDetail({ product, onHome }) {
  const visual = productImages[product.slug];

  return (
    <section className="detail-page">
      <button className="back-button" onClick={() => onHome("catalog")}>返回工具目录</button>

      <article className="detail-hero">
        <div className="detail-media-stage">
          <img src={visual} alt={`${product.name} 产品视觉占位`} />
        </div>
        <div className="detail-copy">
          <div className="detail-kicker">
            <span>{product.index}</span>
            <span>{product.stage}</span>
            <span>{product.openSourceLabel}</span>
          </div>
          <h1>{product.name}</h1>
          <p className="detail-summary">{product.summary}</p>
          <p className="detail-body">{product.detail}</p>
          <div className="detail-actions">
            {product.downloadHref ? <a className="primary-action" href={product.downloadHref}>下载 DMG</a> : <span className="disabled-action">等待发布</span>}
            {product.sourceHref ? <a className="ghost-action" href={product.sourceHref} target="_blank" rel="noreferrer">查看源码</a> : null}
          </div>
        </div>
      </article>

      <div className="detail-grid">
        <DetailList label="主要能力" items={product.highlights} />
        <DetailList label="使用场景" items={product.useCases} />
        <DetailList label="素材状态" items={product.materials} />
      </div>

      <section className="privacy-section">
        <p className="micro-label">BOUNDARY</p>
        <h2>边界先写清楚。</h2>
        <p>{product.privacy}</p>
        <p>{product.releaseNote}</p>
      </section>
    </section>
  );
}

function DetailList({ label, items }) {
  return (
    <section className="detail-block">
      <h2>{label}</h2>
      <ul className="feature-list">
        {items.map((item) => <li key={item}>{item}</li>)}
      </ul>
    </section>
  );
}

function Footer() {
  return (
    <footer className="site-footer">
      <span>{siteMeta.name} · {siteMeta.version}</span>
      <a href={siteMeta.githubHref} target="_blank" rel="noreferrer">xuelinf/nightsailing</a>
    </footer>
  );
}

export default App;
