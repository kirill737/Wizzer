import { useState, useEffect } from "react";
import "../styles/home.scss"
import Header from "../components/Header";
import { Swiper, SwiperSlide } from 'swiper/react';
import { FreeMode, Autoplay, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/free-mode';

function Home() {
  const [burger, setBurger] = useState(false);
  const [categoriesOpened, setCategoriesOpened] = useState(false);
  const [categoriesStep, setCatgeoriesStep] = useState(1);

  return (<>
    <div className="container is-max-widescreen">
      <nav class="navbar" role="navigation" aria-label="main navigation">
        <div id="navbarBasicExample" class="navbar-menu is-justify-content-center">
          <div class="is-flex">
            <div class="navbar-item">
              <button class="button" onClick={() => setCategoriesOpened(!categoriesOpened)}>
                <span class="icon is-small">
                  <i class={`fas fa-${categoriesOpened ? "xmark" : "bars"}`}></i>
                </span>
              </button>
            </div>
            <div className="navbar-item">
              <input class="input" type="text" placeholder="Text input" style={{width: "512px"}} />
            </div>
          </div>
        </div>
      </nav>
    </div>
    <div className="container is-max-widescreen">
      <section className="section">
        {categoriesOpened ?
          <div className="columns">
            <div className="column">
              <aside class="menu">
                <p class="menu-label">Категории</p>
                <ul class="menu-list">
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Смартфоны</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                </ul>
              </aside>
            </div>
            <div className="column">
              {categoriesStep > 1 &&
                <aside class="menu">
                  <p class="menu-label">Бренды</p>
                  <ul class="menu-list">
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Apple</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                </ul>
                </aside>}
            </div>
            <div className="column">
              {categoriesStep > 2 &&
                <aside class="menu">
                  <p class="menu-label">Модели</p>
                  <ul class="menu-list">
                    <li><a href="/model/iPhone 11">iPhone 11</a></li>
                    <li><a href="/model/iPhone 11 Pro">iPhone 11 Pro</a></li>
                    <li><a href="/model/iPhone 11 Pro Max">iPhone 11 Pro Max</a></li>
                    <li><a href="/model/iPhone 12">iPhone 12</a></li>
                    <li><a href="/model/iPhone 12 mini">iPhone 12 mini</a></li>
                    <li><a href="/model/iPhone 12 Pro">iPhone 12 Pro</a></li>
                    <li><a href="/model/iPhone 12 Pro Max">iPhone 12 Pro Max</a></li>
                    <li><a href="/model/iPhone 13">iPhone 13</a></li>
                    <li><a href="/model/iPhone 13 mini">iPhone 13 mini</a></li>
                    <li><a href="/model/iPhone 13 Pro">iPhone 13 Pro</a></li>
                    <li><a href="/model/iPhone 13 Pro Max">iPhone 13 Pro Max</a></li>
                    <li><a href="/model/iPhone 14">iPhone 14</a></li>
                    <li><a href="/model/iPhone 14 Plus">iPhone 14 Plus</a></li>
                    <li><a href="/model/iPhone 14 Pro">iPhone 14 Pro</a></li>
                    <li><a href="/model/iPhone 14 Pro Max">iPhone 14 Pro Max</a></li>
                    <li><a href="/model/iPhone 15">iPhone 15</a></li>
                    <li><a href="/model/iPhone 15 Plus">iPhone 15 Plus</a></li>
                    <li><a href="/model/iPhone 15 Pro">iPhone 15 Pro</a></li>
                    <li><a href="/model/iPhone 15 Pro Max">iPhone 15 Pro Max</a></li>
                    <li><a href="/model/iPhone 16">iPhone 16</a></li>
                    <li><a href="/model/iPhone 16 Plus">iPhone 16 Plus</a></li>
                    <li><a href="/model/iPhone 16 Pro">iPhone 16 Pro</a></li>
                    <li><a href="/model/iPhone 16 Pro Max">iPhone 16 Pro Max</a></li>
                    <li><a href="/model/iPhone 7">iPhone 7</a></li>
                    <li><a href="/model/iPhone SE">iPhone SE</a></li>
                    <li><a href="/model/iPhone X">iPhone X</a></li>
                    <li><a href="/model/iPhone XR">iPhone XR</a></li>
                    <li><a href="/model/iPhone XS">iPhone XS</a></li>
                  </ul>
                </aside>}
            </div>
          </div>
          :
          <Swiper
            slidesPerView={1}
            freeMode={true}
            loop={true}
            spaceBetween={10}
            mousewheel={{
              enabled: true,
              sensitivity: 0.5
            }}
            autoplay={{
              delay: 0,
              disableOnInteraction: false
            }}
            modules={[FreeMode, Mousewheel, Autoplay]}
            speed={20000}
            className="mySwiper"
          >
            <SwiperSlide>
              <div className="fixed-grid has-3-cols m-4">
                <div className="grid">
                  <div className="cell">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-square">
                          <img
                            src="https://bulma.io/assets/images/placeholders/480x480.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-square">
                          <img
                            src="https://bulma.io/assets/images/placeholders/480x480.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell is-row-span-2">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-1-by-2">
                          <img
                            src="https://bulma.io/assets/images/placeholders/320x640.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell is-col-span-2">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-2-by-1">
                          <img
                            src="https://bulma.io/assets/images/placeholders/640x320.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </SwiperSlide>
            <SwiperSlide>
              <div className="fixed-grid has-3-cols m-4">
                <div className="grid">
                  <div className="cell">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-square">
                          <img
                            src="https://bulma.io/assets/images/placeholders/480x480.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-square">
                          <img
                            src="https://bulma.io/assets/images/placeholders/480x480.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell is-row-span-2">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-1-by-2">
                          <img
                            src="https://bulma.io/assets/images/placeholders/320x640.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                  <div className="cell is-col-span-2">
                    <div class="card">
                      <div class="card-image">
                        <figure class="image is-2-by-1">
                          <img
                            src="https://bulma.io/assets/images/placeholders/640x320.png"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </SwiperSlide>
          </Swiper>
        }
      </section>
    </div>
  </>);
}

export default Home;