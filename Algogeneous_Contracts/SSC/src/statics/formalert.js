import { useSelector} from "react-redux";
import ClockLoader from "react-spinners/ClockLoader";

const formalert = () => {
    const darkTheme = useSelector((state) => state.status.darkTheme);
    const { formAlert, alertContent } = useSelector(
      (state) => state.status.formAlert
    );
    return(
        <div
        style={{
            // width: "100%",
          position : "fixed",
          zIndex : "1000",
          bottom: "25px",
          right: "20px",
          display: `${!!formAlert ? "flex" : "none"}`,
          border : "1px solid grey",
          borderRadius : "5px",
          padding : "3px",
          flexDirection: "column",
          background : darkTheme ? "#4a4a4a" : "whitesmoke" ,
          fontWeight: darkTheme ? 400 : 500,
          textTransform: "uppercase",
        }}
        className="confirmation"
      >
        <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <p
                style={{
                  display: "flex",
                  opacity: 0.7,
                  fontWeight: "500",
                  margin: "0px 0px 20px",
                  padding: "5px 11px 4px 2px",
                  textTransform: "uppercase",
                  borderBottom: `2px solid ${darkTheme ? "#eee" : "#222"}`,
                  flexDirection: "row",
                  justifyContent: "space-between"
                }}
              >
                <ClockLoader    
                   color={darkTheme ? "#eee" : "#888"}
                    size={20}
                    width={20}
                    speedMultiplier="0.4" 
                    />

                   <span style={{
                       marginLeft: "5px",
                       color: darkTheme ? "#eee" : "#222"
                   }}> Alert </span>
              </p>

            
                <p style={{
                padding : "1px", 
                fontSize : "11px",
                fontWeight : "bold",
                color : darkTheme ? "#ff4343" : "red",
                    }} 
                className="wallet_content" >
                    {alertContent}
                </p>
            </div>
        {/* <BarLoader
        // style={{marginLeft : "20px"}}
          color={darkTheme ? "#eee" : "#888"}
          size={150}
          width={250}
          speedMultiplier="0.4"
        /> */}

      </div>
    )
}

export default formalert;