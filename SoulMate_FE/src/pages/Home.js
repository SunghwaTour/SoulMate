import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Login from "./Login";

import "../css/App.css";

import image1 from "../Image/Announcement.png";
import BUS from "../Image/bus_45.png";
import School from "../Image/bus_25.png";
import Solaty from "../Image/solaty.png";
import image2 from "../Image/Rectangle 191.png";
import image3 from "../Image/Rectangle 192.png";
import image4 from "../Image/TRP.png";
import image5 from "../Image/KingBusMainLogo.png";

function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  const 게시물목록 = {
    "자유 게시판": [
      "오늘의 출근길 교통상황 공유",
      "내일의 출근길 교통상황 공유",
      "일주일 출근길 날씨상황 공유",
      "일주일 퇴근길 날씨상황 공유",
    ],
    "Q&A 게시판": [
      "운행 시간 관련 질문",
      "노선 변경 문의",
      "예약 취소는 어떻게 하나요?",
      "운행 정지 사유는?",
    ],
    "버스 회사 게시판": [
      "신규 노선 안내",
      "버스 정기점검 일정 안내",
      "운행 기사 모집 공고",
      "차량 정비 비용 안내",
    ],
    "사고 처리 게시판": [
      "사고 처리 절차 안내",
      "사고 관련 보상 정보",
      "보험 적용 여부 확인",
      "사고 처리 문의",
    ],
    "버스 중고 게시판": [
      "중고 버스 판매",
      "중고 버스 구매 요청",
      "버스 관리 방법",
      "중고 시세 정보",
    ],
    "기사 구직 게시판": [
      "운전 기사 구직",
      "운전 경력 공유",
      "구직 정보 등록",
      "근무 조건 안내",
    ],
    "지난주 인기글": ["인기 글 1", "인기 글 2", "인기 글 3"],
  };

  // 스탭 게시물 목록을 객체로 변환하여 연동
  const 스탭게시물목록 = {
    "스탭모집 1": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 2": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 3": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 4": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 5": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 6": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 7": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 8": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 9": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    "스탭모집 10": [
      "스탭 모집 공고 1",
      "스탭 모집 공고 2",
      "스탭 모집 공고 3",
      "스탭 모집 공고 4",
    ],
    스탭프로필: [],
  };

  const 사이드게시물목록 = {
    "지난주 인기글": ["인기 글 1", "인기 글 2", "인기 글 3", "인기 글 4"],
  };

  const 게시판링크 = {
    "자유 게시판": "/board",
    "Q&A 게시판": "/QnAboard",
    "버스 회사 게시판": "/busboard",
    "사고 처리 게시판": "/hitboard",
    "버스 중고 게시판": "/sellboard",
    "기사 구직 게시판": "/driverboard",
  };

  const 게시글링크 = {
    "오늘의 출근길 교통상황 공유": "/today",
  };

  return (
    <div className="App">
      {/* 메인 페이지 */}
      <main>
        <div className="MainHeaderContent">
          <div id="home" className="MainHeader">
            <h1>소울메이트 커뮤니티에 오신 것을 환영합니다!</h1>
            <p>여기에서 다양한 정보와 도움을 얻어가세요.</p>
          </div>

          {/* 알림 섹션 */}
          <div className="announcement">
            <div className="announcement-item">
              <table>
                <tbody>
                  <tr>
                    <td colSpan="2" className="top-td">
                      <img src={image1} alt="알림 이미지" />
                      <a href="">알림</a>
                    </td>
                  </tr>
                  <tr>
                    <td className="body-img">
                      <img src={image2} alt="알림 이미지" />
                    </td>
                    <td className="body-td">
                      <div>
                        <a href="">09/25 소울메이트 커뮤니티 개발</a>
                      </div>
                      <div>
                        <a href="">09/26 커뮤니티 게시판 리액트 코드 변경</a>
                      </div>
                      <div>
                        <a href="">안녕하세요</a>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="announcement-item">
              <table>
                <tbody>
                  <tr>
                    <td colSpan="2" className="top-td">
                      <img src={image1} alt="공지사항 이미지" />
                      <a href="">공지사항</a>
                    </td>
                  </tr>
                  <tr>
                    <td className="body-img">
                      <img src={image3} alt="공지사항 이미지" />
                    </td>
                    <td className="body-td">
                      <div>
                        <a href="">09/25 소울메이트 커뮤니티 개발</a>
                      </div>
                      <div>
                        <a href="">안녕하세요</a>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* 첫 번째 섹션: 자유 게시판, Q&A 게시판 */}
          <div className="board-MainSection">
            {Object.keys(게시물목록).map((boardTitle, index) => (
              <div key={index} className="board">
                <h2>
                  <Link to={게시판링크[boardTitle]}>{boardTitle}</Link>
                </h2>
                <ul>
                  {게시물목록[boardTitle].map((post, idx) => (
                    <li key={idx}>{post}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* 두 번째 섹션: 버스 회사, 사고 처리, 버스 중고 게시판 */}
          <div className="board-SubSection">
            {["버스 회사 게시판", "사고 처리 게시판", "버스 중고 게시판"].map(
              (title, index) => (
                <Board
                  key={index + 2}
                  title={title}
                  posts={게시물목록[title]}
                />
              )
            )}
          </div>

          {/* 세 번째 섹션: 버스 이미지 및 기사 구직 게시판 */}
          <div className="board-LastSection">
            <div className="board">
              <h2>버스</h2>
              <div className="board-Body">
                <div className="column">
                  <a href="">
                    <img src={BUS} alt="버스 이미지" />
                  </a>
                  <p>버스</p>
                </div>
                <div className="column">
                  <a href="">
                    <img src={School} alt="학교 이미지" />
                  </a>
                  <p>학교</p>
                </div>
                <div className="column">
                  <a href="">
                    <img src={Solaty} alt="솔라티 이미지" />
                  </a>
                  <p>솔라티</p>
                </div>
              </div>
            </div>

            <Board
              title="기사 구직 게시판"
              posts={게시물목록["기사 구직 게시판"]}
            />
          </div>

          <div className="ad-section">
            <div className="ad-item">
              <img src={image4} alt="광고 이미지" width="100%" />
            </div>
          </div>

          {/* 스탭 게시판 */}
          <div className="board-MainSection">
            {["스탭모집 1", "스탭모집 2", "스탭모집 3", "스탭모집 4"].map(
              (title, index) => (
                <Step key={index} title={title} posts={스탭게시물목록[title]} />
              )
            )}
          </div>

          {/* 세번째 섹션: 스탭모집5, 스탭모집6, 스탭모집7 */}
          <div className="board-SubSection">
            {["스탭모집 5", "스탭모집 6", "스탭모집 7"].map((title, index) => (
              <Step
                key={index + 2}
                title={title}
                posts={스탭게시물목록[title]}
              />
            ))}
          </div>

          <div className="board-SubSection">
            {["스탭모집 8", "스탭모집 9", "스탭모집 10"].map((title, index) => (
              <Step
                key={index + 2}
                title={title}
                posts={스탭게시물목록[title]}
              />
            ))}
          </div>

          <div className="step-MainSection">
            <div className="Step">
              <h2>스탭프로필</h2>
              <div className="Step-Body">
                <Card></Card>
                <Card></Card>
                <Card></Card>
                <Card></Card>
                <Card></Card>
                <Card></Card>
              </div>
            </div>
          </div>

          <div className="ad-section">
            <div className="ad-item">
              <img src={image4} alt="광고 이미지" width="100%" />
            </div>
          </div>
        </div>
        <div className="SubHeaderContent">
          <div className="sideLogin">
            <Login />

            <div className="video-showcase">
              <h3>필커 온라인 극장</h3>
              {/* Video placeholders */}
              <img src={image3} alt="비디오" />
            </div>

            <Board
              title="지난주 인기글"
              posts={사이드게시물목록["지난주 인기글"]}
            />

            <Board
              title="지난주 인기글"
              posts={사이드게시물목록["지난주 인기글"]}
            />

            <Board
              title="지난주 인기글"
              posts={사이드게시물목록["지난주 인기글"]}
            />

            <Board
              title="지난주 인기글"
              posts={사이드게시물목록["지난주 인기글"]}
            />
          </div>
        </div>
      </main>
      <footer>
        <Footer />
      </footer>
    </div>
  );
}

// 게시판 컴포넌트
function Board({ title, posts }) {
  return (
    <div className="board">
      <h2>{title}</h2>
      <ul>
        {posts.map((post, index) => (
          <li key={index}>
            <Link to={post.link}>{post.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function Step({ title, posts }) {
  return (
    <div className="Step">
      <h2>{title}</h2>
      <ul>
        {posts.map((post, index) => (
          <li key={index}>
            <a href="">{post}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function Card() {
  return (
    <div className="card">
      <div className="top">
        <a href="" class="CardImg">
          <img src={image5} alt="비디오" />
        </a>
      </div>
      <div className="bottom">
        <div className="name">홍길동</div>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <div class="footer-container">
      <div class="footer-left">
        <ul>
          <li>
            <i className="icon"></i>알리는 말씀
          </li>
          <li>
            <i className="icon"></i>이벤트
          </li>
          <li>
            <i className="icon"></i>사이트소개 및 안내
          </li>
          <li>
            <i className="icon"></i>자주묻는 질문들
          </li>
          <li>
            <i className="icon"></i>개인 정보 취급 방침
          </li>
          <li>
            <i className="icon"></i>이용약관
          </li>
        </ul>
      </div>
      <div className="footer-middle">
        <p>
          관리자에게 건의, 요청, 제안 등이 있으시면 민원청구 게시판에
          올려주세요. 이메일이나 전화번호로 요청하시는 답변은 드리지 못합니다.
        </p>
        <button className="complaint-btn">민원청구</button>
      </div>
      <div className="footer-right">
        <p>© 1999 - 2024 SungHwa Community.</p>
      </div>
    </div>
  );
}

export default Home;
