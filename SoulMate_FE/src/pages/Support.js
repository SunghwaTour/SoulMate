import React from "react";

function Support() {
  return (
    <div>
      <h1>지원 페이지</h1>
      <p>성화투어 지원 정보를 확인할 수 있습니다.</p>
      <section>
        <h3>지원 방법</h3>
        <p>성화투어에 지원하는 방법을 안내합니다.</p>
      </section>
      <section>
        <h3>지원서 제출</h3>
        <form>
          <div>
            <label htmlFor="name">이름:</label>
            <input type="text" id="name" name="name" required />
          </div>
          <div>
            <label htmlFor="email">이메일:</label>
            <input type="email" id="email" name="email" required />
          </div>
          <div>
            <label htmlFor="message">문의 사항:</label>
            <textarea id="message" name="message" rows="5" required></textarea>
          </div>
          <button type="submit">제출</button>
        </form>
      </section>
    </div>
  );
}

export default Support;
