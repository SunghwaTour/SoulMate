import React from "react";
import { Link } from "react-router-dom"; // Link는 react-router-dom에서 가져와야 함

const Login = () => {
  return (
    <section id="login">
      <form id="loginForm">
        <div>
          <input
            type="text"
            id="username"
            name="username"
            required
            placeholder="아이디"
          />
        </div>
        <div>
          <input
            placeholder="비밀번호"
            type="password"
            id="password"
            name="password"
            required
          />
        </div>
        <div className="LoginForm">
          <button type="submit" className="login">
            로그인
          </button>
          <Link to="/signup" className="Signup-button">
            회원가입
          </Link>
        </div>
      </form>
      <p id="error-message" className="error"></p>
    </section>
  );
};

export default Login;
