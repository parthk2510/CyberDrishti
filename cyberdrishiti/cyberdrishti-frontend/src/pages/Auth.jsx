import React, { useState } from "react";
import "./styles/Auth.css";
import { motion, AnimatePresence } from "framer-motion"; 
import Squares from "../components/Squares";
import DecryptedText from "../components/DecryptedText";
import ClickSpark from "../components/ClickSpark";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(false);

  const handleToggle = () => setIsLogin((prev) => !prev);

  const fadeAnimation = {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: 0.5, ease: "easeInOut" }
  };

  return (
    <>
      <div className="bg">
        <Squares
          speed={0.5}
          squareSize={40}
          direction="diagonal"
          borderColor="#fff"
          hoverFillColor="#808080"
        />
      </div>

      <div className="auth-screen">
        <div className="container">
          <ClickSpark sparkColor="#fff" sparkSize={10} sparkRadius={15} sparkCount={8} duration={400}>
            <div className="title">
              <DecryptedText
                text="Cyber Drishti"
                animateOn="view"
                revealDirection="center"
              />
            </div>

            <div className="button-switch">
              <button
                className={!isLogin ? "active" : ""}
                onClick={() => setIsLogin(false)}
              >
                Sign Up
              </button>
              <button
                className={isLogin ? "active" : ""}
                onClick={() => setIsLogin(true)}
              >
                Login
              </button>
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={isLogin ? "login" : "signup"}
                {...fadeAnimation}
                className="inner-container"
              >
                <div className="forms">
                  <input
                    type="text"
                    name="email"
                    placeholder="Email"
                    id="email"
                  />
                  <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    id="password"
                  />
                  {!isLogin && (
                    <input
                      type="password"
                      name="confirm-password"
                      placeholder="Confirm Password"
                      id="confirm-password"
                    />
                  )}
                </div>

                <div className="buttons">
                  {!isLogin && (
                    <button id="signup" onClick={() => setIsLogin(false)}>
                      Sign Up
                    </button>
                  )}
                  {isLogin && (
                    <button id="signin" onClick={() => setIsLogin(true)}>
                      Sign In
                    </button>
                  )}
                </div>
              </motion.div>
            </AnimatePresence>
          </ClickSpark>
        </div>
      </div>
    </>
  );
};

export default Auth;
