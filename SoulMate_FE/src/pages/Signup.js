import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/Signup.css";

function Signup() {
  const navigate = useNavigate();

  const handleCancel = () => {
    navigate("/");
  };

  const TextField = ({ label, placeholder, type = "text" }) => {
    const [inputValue, setInputValue] = useState("");

    const handleInputChange = (event) => {
      setInputValue(event.target.value);
      console.log(event.target.value); // 입력된 값을 콘솔에 출력
    };

    return (
      <div className="form-group">
        <div className="group-Name">{label}</div>
        <input
          type={type}
          placeholder={placeholder}
          value={inputValue}
          onChange={handleInputChange}
        />
      </div>
    );
  };

  return (
    <div className="signup-container">
      <h2>회원가입</h2>
      <form className="signup-form">
        <TextField
          label="아이디"
          placeholder="아이디를 입력해주세요."
          type="id"
        />
        <TextField
          label="비밀번호"
          type="password"
          placeholder="비밀번호를 입력해주세요."
        />
        <TextField
          label="비밀번호 확인"
          type="password"
          placeholder="비밀번호를 재입력해주세요."
        />
        <TextField label="이메일" placeholder="이메일을 입력해주세요." />
        <TextField label="전화번호" placeholder="전화번호를 입력해주세요." />
        <TextField label="이름" placeholder="이름을 입력해주세요." />
        <TextField label="닉네임" placeholder="닉네임을 입력해주세요." />
        <div className="button-Sign">
          <button
            type="button"
            className="Signup-Button Cancellation"
            onClick={handleCancel}
          >
            취소
          </button>
          <button type="submit" className="Signup-Button Registration">
            등록
          </button>
        </div>
      </form>
    </div>
  );
}

export default Signup;
