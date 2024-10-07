import { useState, useEffect } from "react";
import "../styles/header.scss"
import logo from "../assets/react.svg"

function Header() {
    const [burger, setBurger] = useState(false);
    const [categoriesOpened, setCategoriesOpened] = useState(false);

    return (
        <div className="container is-max-widescreen">
            <nav class="navbar" role="navigation" aria-label="main navigation">
                <div id="navbarBasicExample" class="navbar-menu is-justify-content-center">
                    <div class="is-flex">
                        <div class="navbar-item">
                            <button class="button" onClick={() => setCategoriesOpened(true)}>
                                <span class="icon is-small">
                                    <i class="fas fa-bars"></i>
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
    );
}

export default Header;