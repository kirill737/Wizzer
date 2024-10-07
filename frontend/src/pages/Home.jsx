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
              <input class="input" type="text" placeholder="Text input" />
            </div>
            <div class="navbar-item">
              <button class="button">
                <span class="icon is-small">
                  <i class="fas fa-heart"></i>
                </span>
              </button>
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
                      <span>Категория</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Категория</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Категория</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Категория</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Категория</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(2)}>
                    <span className="icon-text">
                      <span>Категория</span>
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
                      <span>Бренд</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Бренд</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Бренд</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Бренд</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Бренд</span>
                      <span className="icon">
                        <i className="fas fa-chevron-right"></i>
                      </span>
                    </span>
                  </a></li>
                  <li><a onClick={() => setCatgeoriesStep(3)}>
                    <span className="icon-text">
                      <span>Бренд</span>
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
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
                    <li><a>Модель</a></li>
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