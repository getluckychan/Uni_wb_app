import React, { Component } from "react";

class Header extends Component {
  render() {
    return (
      <div className="text-center">
        <img
          src="https://logrocket-assets.io/img/logo.png"
          width="300"
          className="img-thumbnail"
          style={{ marginTop: "20px" }}
        />
        <hr />
        <h5>
          <i>presents</i>
        </h5>
        <h1>App with React + Django</h1>
      </div>
    );
  }
}

const SearchBar = ({onSearchSubmit}) => {
    return (
      <div className='searchbar'>
        <input
            className='searchbar-input'
            type='text'
            placeholder="Search user by name. . ."/>
      </div>
    );
};

export default Header;
