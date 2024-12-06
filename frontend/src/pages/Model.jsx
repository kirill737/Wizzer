import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api"
import "../styles/home.scss"
import Header from "../components/Header";
import { Swiper, SwiperSlide } from 'swiper/react';
import { FreeMode, Autoplay, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/free-mode';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  PieController,
  ArcElement,
  RadarController,
  RadialLinearScale,
  Filler
} from 'chart.js';
import { Pie, Radar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  PieController,
  ArcElement,
  RadarController,
  RadialLinearScale
);


const pie_options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  stacked: false,
  plugins: {
    title: {
      display: true,
      text: 'Оценки пользователей'
    }
  }
};
const pie_labels = [1, 2, 3, 4, 5];


const radar_options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  stacked: false,
  plugins: {
    title: {
      display: true,
      text: 'Сравнение со средним'
    }
  }
};
const radar_labels = ["Скорость", "Камера", "Цена"];



function Model() {
  const params = useParams();

  const [burger, setBurger] = useState(false);
  const [categoriesOpened, setCategoriesOpened] = useState(false);
  const [categoriesStep, setCatgeoriesStep] = useState(1);
  const [searchDropdown, setSearchDropdown] = useState(false);
  const [selectTopRating, setSelectTopRating] = useState(true)

  const [priceOrder, setPriceOrder] = useState([]);
  const [ratingOrder, setRatingOrder] = useState([]);
  const [ratingData, setRatingData] = useState([]);
  const [characteristics, setCharacteristics] = useState([]);
  const [radarData, setRadarData] = useState([]);
  const [meanPrice, setMeanPrice] = useState(0);
  const [meanRating, setMeanRating] = useState(0);
  const [selectedDeal, setSelectedDeal] = useState(null);

  useEffect(() => {
    getDeviceInfo();
  }, [])

  useEffect(() => {
    if (selectedDeal) setRadarData([selectedDeal.Процессор, selectedDeal.Камера, selectedDeal.Цена])
  }, [selectedDeal])

  const getDeviceInfo = async () => {
    try {
      const res = await api.post("device", {"user_query": params.query, "top_k": 50});
      if (res.status === 200) {
          setPriceOrder(res.data.price_order)
          setRatingOrder(res.data.rating_order)
          setSelectedDeal(res.data.rating_order[0])
          setRadarData([res.data.rating_order[0].Процессор, res.data.rating_order[0].Камера, res.data.rating_order[0].Цена])
          const ratings = []
          ratings.push(res.data.statistics["1"])
          ratings.push(res.data.statistics["2"])
          ratings.push(res.data.statistics["3"])
          ratings.push(res.data.statistics["4"])
          ratings.push(res.data.statistics["5"])
          setRatingData(ratings)
          const chars = []
          chars.push(res.data.statistics["mean_Процессор"])
          chars.push(res.data.statistics["mean_Камера"])
          chars.push(res.data.statistics["mean_Цена"])
          setCharacteristics(chars)
          setMeanPrice(res.data.statistics.mean_price)
          setMeanRating(res.data.statistics.mean_non_zero_rating)
      }
    } catch (error) {
        console.log(error);
    }
  }

  const pie_data = {
    labels: pie_labels,
    datasets: [{
      label: 'Оценки пользователей',
      data: ratingData,
      backgroundColor: [
        'rgb(230, 124, 115)',
        'rgb(243, 169, 109)',
        'rgb(255, 214, 102)',
        'rgb(171, 201, 120)',
        'rgb(87, 187, 138)'
      ],
      hoverOffset: 4
    }]
  };

  const radar_data = {
    labels: radar_labels,
    datasets: [{
      label: 'Выбранное предложение',
      data: radarData,
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }, {
      label: 'Среднее',
      data: characteristics,
      fill: true,
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgb(54, 162, 235)',
      pointBackgroundColor: 'rgb(54, 162, 235)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(54, 162, 235)'
    }]
  };

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

              <div class={`dropdown ${searchDropdown ? "is-active" : ""}`}>
                <div class="dropdown-trigger">
                  <input class="input" type="text" placeholder="Text input" aria-haspopup="true" aria-controls="dropdown-menu" style={{ width: "512px" }} onClick={() => setSearchDropdown(!searchDropdown)} />
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu" style={{ width: "512px" }}>
                  <div class="dropdown-content">
                    <div class="list">
                      <div class="list-item">
                        <div class="list-item-title">List item</div>
                      </div>

                      <div class="list-item">
                        <div class="list-item-title">List item</div>
                      </div>

                      <div class="list-item">
                        <div class="list-item-content">
                          <div class="list-item-title">List item</div>
                          <div class="list-item-description">List item description</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

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
          <>
            <h1 className="title">{params.query}</h1>
            <div class="columns">
              <div class="column is-half">
                <div className="box">
                  <h4 class="title is-4">Скорость</h4>
                  <progress class={`progress ${characteristics[0] < -0.5 ? "is-danger" : characteristics[0] > 0.5 ? "is-success": "is-warning"}`} value={`${characteristics[0]+1}`} max="2" />
                  <h4 class="title is-4">Камера</h4>
                  <progress class={`progress ${characteristics[1] < -0.5 ? "is-danger" : characteristics[1] > 0.5 ? "is-success": "is-warning"}`} value={`${characteristics[1]+1}`} max="2" />
                  <h4 class="title is-4">Цена</h4>
                  <progress class={`progress ${characteristics[2] < -0.5 ? "is-danger" : characteristics[2] > 0.5 ? "is-success": "is-warning"}`} value={`${characteristics[2]+1}`} max="2" />
                </div>
              </div>
              <div class="column is-half">
                {selectedDeal && 
                <div className="box">
                  <div className="columns has-text-centered">
                    <div className="column my-auto">
                      <p className="attribute-name">Ср. рейтинг</p>
                      <span class="icon-text is-size-5">
                        <span>{meanRating.toFixed(2)}</span>
                        <span class="icon has-text-warning">
                          <i class="fas fa-star"></i>
                        </span>
                      </span>
                    </div>
                    <div className="column my-auto">
                      <div class="field has-addons">
                        <p class="control">
                          <button class={`button is-primary ${selectTopRating ? "is-active" : "" }`} onClick={() => {setSelectTopRating(true); setSelectedDeal(ratingOrder[0])}}>
                            <span class="icon is-small">
                              <i class="fas fa-arrow-up"></i>
                            </span>
                            <span>Рейтинг</span>
                          </button>
                        </p>
                        <p class="control">
                          <button class={`button is-link ${!selectTopRating ? "is-active" : "" }`} onClick={() => {setSelectTopRating(false); setSelectedDeal(priceOrder[0])}}>
                            <span class="icon is-small">
                              <i class="fas fa-arrow-down"></i>
                            </span>
                            <span>Цена</span>
                          </button>
                        </p>
                      </div>
                    </div>
                    <div className="column my-auto">
                      <p className="attribute-name">Ср. цена</p>
                      <h5 className="title is-5">{meanPrice.toLocaleString()} ₽</h5>
                    </div>
                  </div>
                  <div className="has-text-centered">
                    <p className="attribute-name">{selectTopRating ? "Предложение с наибольшим рейтингом" : "Самое дешёвое предложение"}</p>
                  </div>
                  <h5 className="title is-5 mt-3 has-text-centered">{selectedDeal.fullname}</h5>
                  <div className="attribute mt-5">
                    <span className="attribute-name">Рейтинг</span>
                    <span className="dots"></span>
                    <span className="attribute-value">
                      <span class="icon-text">
                        <span>{selectedDeal.rating}</span>
                        <span class="icon has-text-warning">
                          <i class="fas fa-star"></i>
                        </span>
                      </span>
                    </span>
                  </div>
                  <div className="attribute mt-5">
                    <span className="attribute-name">Цена</span>
                    <span className="dots"></span>
                    <span className="attribute-value">{selectedDeal.price.toLocaleString()} ₽</span>
                  </div>
                  <div className="has-text-centered">
                    <a href={selectedDeal.link} target="_blank" className="attribute-name is-underlined">Ссылка</a>
                  </div>
                </div>
                }
              </div>
            </div>
            <div className="columns">
              <div className="column is-half">
                <div className="box" style={{ height: "400px" }}>
                  <Pie options={pie_options} data={pie_data} />
                </div>
              </div>
              <div className="column is-half">
                <div className="box" style={{ height: "400px" }}>
                  <Radar options={radar_options} data={radar_data} />
                </div>
              </div>
            </div>
            <div className="columns">
              <div className="column is-one-third">
                <h3 className="title is-3">Топ предложений</h3>
              </div>
              <div className="column">
                <div class="tabs">
                  <ul>
                    <li class={`${selectTopRating ? "is-active" : "" }`} onClick={() => {setSelectTopRating(true); setSelectedDeal(ratingOrder[0])}}><a>По рейтингу</a></li>
                    <li class={`${!selectTopRating ? "is-active" : "" }`} onClick={() => {setSelectTopRating(false); setSelectedDeal(priceOrder[0])}}><a>По цене</a></li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="list has-hoverable-list-items">
              { selectTopRating ?
              ratingOrder.length > 0 ?
              ratingOrder.map((d) => <a href={d.link} target="_blank" class="list-item box is-clickable">
              <div class="list-item-image has-text-centered">
                <span class="icon-text is-size-5">
                  <span>{d.rating}</span>
                  <span class="icon has-text-warning">
                    <i class="fas fa-star"></i>
                  </span>
                </span>
                <h5 className="title is-5 mt-1">{d.price.toLocaleString()} ₽</h5>
              </div>
              <div class="list-item-content">
                <div class="list-item-title">{d.fullname}</div>
                <div class="list-item-description">Перейти на сайт</div>
              </div>
            </a>)
            : <></>
            :
            priceOrder.length > 0 ?
            priceOrder.map((d) => <a href={d.link} target="_blank" class="list-item box is-clickable">
            <div class="list-item-image has-text-centered">
              <span class="icon-text is-size-5">
                <span>{d.rating}</span>
                <span class="icon has-text-warning">
                  <i class="fas fa-star"></i>
                </span>
              </span>
              <h5 className="title is-5 mt-1">{d.price.toLocaleString()} ₽</h5>
            </div>
            <div class="list-item-content">
              <div class="list-item-title">{d.fullname}</div>
              <div class="list-item-description">Перейти на сайт</div>
            </div>
          </a>)
          : <></>
              }
            </div>
          </>
        }
      </section>
    </div>
  </>);
}

export default Model;