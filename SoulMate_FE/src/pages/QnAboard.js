import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/QnAboard.css";

const QnAboard = () => {
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const postsPerPage = 5;
  const pageLimit = 5;

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          "https://jsonplaceholder.typicode.com/posts"
        ); // 실제 API URL로 변경
        setPosts(response.data);
        setLoading(false);
      } catch (err) {
        setError("데이터를 불러오는 데 실패했습니다.");
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = posts.slice(indexOfFirstPost, indexOfLastPost);

  const totalPages = Math.ceil(posts.length / postsPerPage);
  const [currentPageGroup, setCurrentPageGroup] = useState(1);
  const totalPageGroups = Math.ceil(totalPages / pageLimit);

  const getPageNumbers = () => {
    const start = (currentPageGroup - 1) * pageLimit + 1;
    const end = Math.min(start + pageLimit - 1, totalPages);
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const goToNextPageGroup = () => {
    if (currentPageGroup < totalPageGroups) {
      setCurrentPageGroup(currentPageGroup + 1);
      setCurrentPage((currentPageGroup + 1 - 1) * pageLimit + 1);
    }
  };

  const goToPreviousPageGroup = () => {
    if (currentPageGroup > 1) {
      setCurrentPageGroup(currentPageGroup - 1);
      setCurrentPage((currentPageGroup - 1) * pageLimit + 1);
    }
  };

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="qna-page">
      <h1>Q&A 게시판</h1>
      <ul className="post-list">
        {currentPosts.map((post) => (
          <li key={post.id} className="post-item">
            {post.title}
          </li>
        ))}
      </ul>
      <div className="pagination">
        <button
          className="pagination-button"
          onClick={goToPreviousPageGroup}
          disabled={currentPageGroup === 1}
        >
          &lt;
        </button>
        {getPageNumbers().map((number) => (
          <button
            key={number}
            onClick={() => paginate(number)}
            className={`pagination-button ${
              number === currentPage ? "active" : ""
            }`}
          >
            {number}
          </button>
        ))}
        <button
          className="pagination-button"
          onClick={goToNextPageGroup}
          disabled={currentPageGroup === totalPageGroups}
        >
          &gt;
        </button>
      </div>
    </div>
  );
};

export default QnAboard;
