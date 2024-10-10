import React, { useRef, useState } from "react";
import emailjs from "@emailjs/browser";
import { useNavigate } from "react-router-dom"; // 페이지 이동을 위해 import
import "../css/Contact.css";

function Contact() {
  const form = useRef();
  const [messageSent, setMessageSent] = useState(false);
  const navigate = useNavigate();

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        "service_7poofnk", // EmailJS 서비스 ID
        "template_sgxzoud", // EmailJS 템플릿 ID
        form.current,
        "N9vqPGIe6rrRvXMH5" // EmailJS 사용자 ID (Public Key)
      )
      .then(
        (result) => {
          console.log(result.text);
          setMessageSent(true);
        },
        (error) => {
          console.log(error.text);
          setMessageSent(false);
        }
      );
  };

  const handleClosePopup = () => {
    setMessageSent(false);
    navigate("/"); // 메인 페이지로 이동
  };

  return (
    <div className="Contact-container">
      <div className="contact-MainHeader">
        <h1>문의하기</h1>
      </div>

      {messageSent && (
        <div className="popup">
          <div className="popup-content">
            <p>메시지가 성공적으로 전송되었습니다!</p>
            <button onClick={handleClosePopup}>확인</button>
          </div>
        </div>
      )}

      <form ref={form} onSubmit={sendEmail} className="Contact-MainBody">
        <div>
          <label htmlFor="name">문의유형 (필수)</label>
          <input
            type="text"
            id="name"
            name="name"
            required
            placeholder="서비스를 입력해주세요."
          />
        </div>
        <hr />
        <div>
          <label htmlFor="title">제목 (필수)</label>
          <input
            type="text"
            id="title"
            name="title"
            required
            placeholder="제목을 입력해주세요."
          />
        </div>
        <hr />
        <div>
          <label htmlFor="message">내용 (필수)</label>
          <textarea
            id="message"
            name="message"
            rows="5"
            required
            placeholder="내용을 입력해주세요."
          ></textarea>
        </div>
        <hr />
        <div>
          <label htmlFor="email">이메일 (필수)</label>
          <input
            type="email"
            id="email"
            name="email"
            required
            placeholder="이메일을 입력해주세요."
          />
        </div>
        <hr />
        <div>
          <label htmlFor="phone">전화번호 (필수)</label>
          <input
            type="text"
            id="phone"
            name="phone"
            required
            placeholder="전화번호를 입력해주세요"
          />
        </div>
        <hr />
        <div className="Contact-DivBtn">
          <button className="Contact-Btn" type="submit">
            제출
          </button>
        </div>
      </form>
    </div>
  );
}

export default Contact;
