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

const principles = [
  {
    label: "Collect",
    title: "把可用的留下",
    body: "这里不是灵感墙，而是经过自己长期使用、打磨、发布的工具目录。",
  },
  {
    label: "Open",
    title: "能开源的就开源",
    body: "当工具适合共享，会留下源码入口；当还在形成，会先清楚标注状态。",
  },
  {
    label: "Quiet",
    title: "让技术降低噪声",
    body: "AI 工具不需要总是耀眼。它更像夜里的一盏灯，照见下一步即可。",
  },
];

const routeStops = [
  "发现一个真实的小问题",
  "把流程压缩成一个工具",
  "发布下载与源码入口",
  "继续记录下一次改版",
];

function getInitialSlug() {
  const match = window.location.hash.match(/^#\/product\/(.+)$/);
  return match ? decodeURIComponent(match[1]) : "";
}

function App() {
  const [activeSlug, setActiveSlug] = useState(getInitialSlug);
  const [scrollRatio, setScrollRatio] = useState(0);
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

  useEffect(() => {
    const updateScrollRatio = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      setScrollRatio(maxScroll > 0 ? window.scrollY / maxScroll : 0);
    };
    updateScrollRatio();
    window.addEventListener("scroll", updateScrollRatio, { passive: true });
    window.addEventListener("resize", updateScrollRatio);
    return () => {
      window.removeEventListener("scroll", updateScrollRatio);
      window.removeEventListener("resize", updateScrollRatio);
    };
  }, [activeSlug]);

  useEffect(() => {
    const targets = document.querySelectorAll("[data-reveal]");
    if (!("IntersectionObserver" in window)) {
      targets.forEach((target) => target.classList.add("is-visible"));
      return undefined;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 },
    );

    targets.forEach((target) => observer.observe(target));
    return () => observer.disconnect();
  }, [activeSlug]);

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
      <ScrollProgress value={scrollRatio} />
      <Nav onHome={goHome} />
      {activeProduct ? (
        <ProductDetail product={activeProduct} onHome={goHome} />
      ) : (
        <Home onOpenProduct={openProduct} />
      )}
    </main>
  );
}

function ScrollProgress({ value }) {
  return <div className="scroll-progress" style={{ transform: `scaleX(${value})` }} />;
}

function Nav({ onHome }) {
  return (
    <header className="site-nav">
      <nav className="nav-links" aria-label="主导航">
        <button onClick={() => onHome("preface")}>序章</button>
        <button onClick={() => onHome("catalog")}>船舱</button>
        <button onClick={() => onHome("route")}>航线</button>
      </nav>
      <button className="brand-mark" onClick={() => onHome()} aria-label="回到首页">
        <span>夜航船</span>
      </button>
      <div className="nav-actions">
        <a href={siteMeta.githubHref} target="_blank" rel="noreferrer">GitHub</a>
        <button className="filled-link" onClick={() => onHome("catalog")}>打开目录</button>
      </div>
    </header>
  );
}

function Home({ onOpenProduct }) {
  const availableCount = products.filter((product) => product.status === "available").length;
  const plannedCount = products.length - availableCount;

  return (
    <>
      <section className="hero-section" id="preface">
        <img className="hero-image" src={heroImage} alt="" />
        <div className="hero-shade" />
        <div className="hero-ornament" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>

        <div className="hero-copy" data-reveal>
          <p className="micro-label">{siteMeta.edition}</p>
          <h1>{siteMeta.name}</h1>
          <p className="hero-line">{siteMeta.headline}</p>
          <p className="hero-text">
            一艘安静的船，收纳那些被做出来、被验证过、也仍在生长的 AI 工具。
            每一个舱位都指向一个具体问题：下载、源码、日志和下一次改版。
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#catalog">查看船舱</a>
            <a className="ghost-action" href="#route">阅读航线</a>
          </div>
        </div>

        <div className="hero-ledger" data-reveal>
          <span>TOOLS {String(products.length).padStart(2, "0")}</span>
          <span>OPEN {String(availableCount).padStart(2, "0")}</span>
          <span>NEXT {String(plannedCount).padStart(2, "0")}</span>
        </div>
      </section>

      <section className="principle-section" aria-label="夜航船之书的原则">
        {principles.map((item) => (
          <article className="principle-card" key={item.label} data-reveal>
            <span>{item.label}</span>
            <h2>{item.title}</h2>
            <p>{item.body}</p>
          </article>
        ))}
      </section>

      <section className="catalog-section" id="catalog">
        <div className="section-heading" data-reveal>
          <div>
            <p className="micro-label">CABIN INDEX</p>
            <h2>船舱不是货架，是工具的陈列室。</h2>
          </div>
          <p>
            卡片记录当前状态、下载入口与开源边界。能使用的直接上船；
            还在设计中的，也先留下清楚的位置。
          </p>
        </div>
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.slug} product={product} onOpen={() => onOpenProduct(product.slug)} />
          ))}
        </div>
      </section>

      <section className="route-section" id="route">
        <div className="route-copy" data-reveal>
          <p className="micro-label">BUILD ROUTE</p>
          <h2>从一个具体的麻烦，航行到一个可被取用的工具。</h2>
        </div>
        <ol className="route-list">
          {routeStops.map((stop, index) => (
            <li key={stop} data-reveal>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <p>{stop}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="log-section" id="log">
        <div className="section-heading compact" data-reveal>
          <div>
            <p className="micro-label">LOGBOOK</p>
            <h2>最近一次校订</h2>
          </div>
          <p>把首版从“能看见”推进到“有调性、有交互、能展示”。</p>
        </div>
        <div className="log-list">
          <article data-reveal><span>0.0.2</span><p>重做首页叙事、产品卡片、滚动显现、详情页媒体舞台和产品视觉占位。</p></article>
          <article data-reveal><span>0.0.1</span><p>建立“夜航船之书”站点、四个产品位和两个 macOS 工具下载入口。</p></article>
        </div>
      </section>

      <Footer />
    </>
  );
}

function ProductCard({ product, onOpen }) {
  const isAvailable = product.status === "available";

  function handleKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onOpen();
    }
  }

  function handlePointerMove(event) {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width;
    const y = (event.clientY - rect.top) / rect.height;
    event.currentTarget.style.setProperty("--pointer-x", `${x * 100}%`);
    event.currentTarget.style.setProperty("--pointer-y", `${y * 100}%`);
    event.currentTarget.style.setProperty("--tilt-x", `${(0.5 - y) * 7}deg`);
    event.currentTarget.style.setProperty("--tilt-y", `${(x - 0.5) * 7}deg`);
    event.currentTarget.style.setProperty("--lift", "-8px");
  }

  function resetPointer(event) {
    event.currentTarget.style.removeProperty("--tilt-x");
    event.currentTarget.style.removeProperty("--tilt-y");
    event.currentTarget.style.removeProperty("--lift");
  }

  return (
    <article
      className={`product-card ${isAvailable ? "is-available" : "is-planned"}`}
      role="button"
      tabIndex="0"
      onClick={onOpen}
      onKeyDown={handleKeyDown}
      onPointerMove={handlePointerMove}
      onPointerLeave={resetPointer}
      data-reveal
    >
      <div className="card-visual">
        <img src={productImages[product.slug]} alt="" />
      </div>
      <div className="card-body">
        <div className="card-meta">
          <span>{product.index}</span>
          <span>{product.statusLabel}</span>
          <span>{product.openSourceLabel}</span>
        </div>
        <h3>{product.name}</h3>
        <p>{product.summary}</p>
      </div>
      <div className="card-foot">
        <span>{product.platform}</span>
        <span>{isAvailable ? "进入发布页" : "查看预告"}</span>
      </div>
    </article>
  );
}

function ProductDetail({ product, onHome }) {
  const isAvailable = product.status === "available";
  const visual = productImages[product.slug];

  return (
    <section className="detail-page">
      <button className="back-button" onClick={() => onHome("catalog")}>返回船舱目录</button>

      <article className="detail-hero" data-reveal>
        <div className="detail-copy">
          <div className="detail-kicker">
            <span>{product.index}</span>
            <span>{product.stage}</span>
            <span>{product.openSourceLabel}</span>
          </div>
          <h1>{product.name}</h1>
          <p className="detail-manifesto">{product.manifesto}</p>
          <p className="detail-summary">{product.detail}</p>
          <div className="detail-actions">
            {product.downloadHref ? <a className="primary-action" href={product.downloadHref}>下载 DMG</a> : <span className="disabled-action">等待首航</span>}
            {product.sourceHref ? <a className="ghost-action" href={product.sourceHref} target="_blank" rel="noreferrer">查看源码</a> : null}
            <a className="ghost-action" href="#media">查看素材位</a>
          </div>
        </div>
        <div className="detail-media-stage">
          <img src={visual} alt={`${product.name} 产品视觉占位`} />
          <div className="stage-caption">
            <span>{product.shortName}</span>
            <span>{isAvailable ? "Release Visual" : "Concept Visual"}</span>
          </div>
        </div>
      </article>

      <div className="detail-grid">
        <section className="detail-block" data-reveal>
          <p className="micro-label">WHAT IT DOES</p>
          <h2>它要解决的问题</h2>
          <ul className="feature-list">
            {product.features.map((feature) => <li key={feature}>{feature}</li>)}
          </ul>
        </section>
        <section className="detail-block" data-reveal>
          <p className="micro-label">WHEN TO USE</p>
          <h2>它出现的场景</h2>
          <ul className="feature-list">
            {product.scenes.map((scene) => <li key={scene}>{scene}</li>)}
          </ul>
        </section>
      </div>

      <section className="media-section" id="media" data-reveal>
        <div className="media-heading">
          <p className="micro-label">MEDIA DOCK</p>
          <h2>截图和视频会停靠在这里。</h2>
          <p>当前先放概念视觉，后续替换为真实产品截图、视频演示和发布说明。</p>
        </div>
        <div className="media-grid">
          {product.mediaSlots.map((slot, index) => (
            <article key={slot} className="media-slot">
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{slot}</h3>
              <p>{index === 0 ? product.releaseNote : "等待真实素材补入后，这里会成为产品页的核心展示段落。"}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="privacy-section" data-reveal>
        <p className="micro-label">BOUNDARY</p>
        <h2>边界先写清楚，工具才值得被信任。</h2>
        <p>{product.privacy}</p>
        {!isAvailable ? <p className="planned-note">这个舱位仍在建造中，因此不会伪造下载或源码状态。</p> : null}
      </section>
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
