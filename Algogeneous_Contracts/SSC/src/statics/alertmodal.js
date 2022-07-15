import { useSelector, useDispatch } from "react-redux";
import HashLoader from "react-spinners/HashLoader";

const AlertModal = () => {
  const darkTheme = useSelector((state) => state.status.darkTheme);

  const dispatch = useDispatch();

  const { openModal, modalContent,percentage ,txId} = useSelector(
    (state) => state.status.alertModal
  );

  return (
    <menu
      className="mn_sm"
      style={{ display: `${!!openModal ? "flex" : "none"}` }}
    >
      <div className="mn_sm_modal">
        <div
          style={{
            width: "100%",
            display: "flex",
            marginRight: "10px",
            flexDirection: "row",
            justifyContent: "flex-end",
          }}
        >
          <div
            style={{
              width: "50px",
              height: "50px",
              display: "flex",
              fontSize: "16px",
              cursor: "pointer",
              fontWeight: "500",
              textAlign: "center",
              borderRadius: "100%",
              alignItems: "center",
              justifyContent: "center",
              textTransform: "uppercase",
              border: "1px solid var(--l1)",
              background: "var(--main-col)",
            }}
            onClick={() => {
              dispatch({ type: "close_modal" });
            }}
          >
            <i className="uil uil-times"></i>
          </div>
        </div>

        <div
          className="mn_sm_modal_inn"
          style={{
            color: darkTheme ? "#fff" : "#000",
            background: darkTheme ? "#4a4a4a" : "#f2f2f2",
          }}
        >
          <>
            <div
              style={{
                minHeight: "100px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
             
              <p
                style={{
                  opacity: 0.7,
                  fontWeight: "500",
                  margin: "0px 0px 20px",
                  padding: "14px 10px 7px 2px",
                  textTransform: "uppercase",
                  borderBottom: `2px solid ${darkTheme ? "#eee" : "#222"}`,
                  display: "flex",
                  flexDirection: "row"
                }}
              >
                <HashLoader 
                       color={darkTheme ? "#eee" : "#888"}
                       size={17}
                       width={17}
                       speedMultiplier="0.4"
                />

               <span style={{
                 marginRight: "5px"
               }}> Result</span> 
              </p>
            <div style={{
              display: "flex",
              textAlign: "left",
              justifyContent: "left",
              flexDirection: "column"
            }}>
            <p
                style={{
                  opacity: 0.7,
                  textAlign: "center",
                  lineHeight: "25px",
                  marginBottom: "10px",
                }}
              >
                {modalContent}
              </p>


              <p style={{
                  opacity: 0.7,
                marginTop: "-5px",
                lineHeight: "25px",
              }}> 
                Percentage : <span
                  style={{
                    color: percentage < 50 ? "red" : "#09b109"
                  }}       
                >
                  {percentage}% 

                </span>
                
                {/* {
                  percentage < 30 ? (<i 
                     style={{}}
                    class="uil uil-thumbs-down"></i>) 
                  : (<i 
                      style={{
                        marginRight: "3px",
                        color: "yellow"
                      }}
                    class="uil uil-thumbs-up"> </i>)
                } */}
              </p>

              <a
               href={`https://testnet.algoexplorer.io/tx/${txId}`}
               style={{
                opacity: 0.7,
                lineHeight: "25px",
                color:"blue",
                marginBottom: "10px",
              }}>
                view on algoexplorer <i className="uil uil-arrow-up-right"></i>
              </a>
            </div>
          
            </div>
          </>
        </div>
      </div>
    </menu>
  );
};

export default AlertModal;
