import * as React from "react";
import { useState } from "react";
import Cell from "./Cell";
import Loading from "./Loading";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "./Modal";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const size = 5;

const request = {
  result: [3, 2, 1, 1, 3, 2, 2, 1, 3],
  values: [
    {
      bottom: 0,
      left: 0,
      right: 0,
      top: 0,
      value: "*3",
    },
    {
      bottom: 0,
      left: 0,
      right: 1,
      top: 0,
      value: "0",
    },
    {
      bottom: 1,
      left: 1,
      right: 0,
      top: 0,
      value: "+4",
    },
    {
      bottom: 1,
      left: 0,
      right: 1,
      top: 0,
      value: "*12",
    },
    {
      bottom: 1,
      left: 1,
      right: 0,
      top: 0,
      value: "0",
    },
    {
      bottom: 0,
      left: 0,
      right: 0,
      top: 1,
      value: "0",
    },
    {
      bottom: 0,
      left: 0,
      right: 1,
      top: 1,
      value: "0",
    },
    {
      bottom: 0,
      left: 1,
      right: 0,
      top: 1,
      value: "0",
    },
    {
      bottom: 0,
      left: 0,
      right: 0,
      top: 0,
      value: "*3",
    },
  ],
};

const App = () => {
  const [cells, setCells] = useState();
  const [result, setResult] = useState({});
  const [solve, setSolve] = useState(false);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const handleOnChange = (value, index) => {
    // console.log("hi", value, index);
    setResult({ ...result, [index]: value });
  };

  const handleSubmit = () => {
    console.log("zepy");
    setSolve(false);
    if (Object.keys(result).length != cells?.result.length)
      toast.error("🦄 Please enter valus for all cells!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    else {
      for (let i = 0; i < cells?.result.length; i++)
        if (result[i] != cells?.result[i]) {
          toast.error("Wrong Answer!", {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
          });
          return;
        }
      toast.success("Right Answer, Good Job!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      //TODO : clear after submit
    }
  };

  const handleSolve = () => {
    toast.info("Solved!", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });
    setSolve(true);
  };

  const hanldeGenerate = async (info) => {
    setSolve(false);
    console.log("gene", info);
    //TODO: validate before API Call
    if (!("size" in info && "algorithm" in info)) {
      toast.error("🦄 Please enter both algorithm and size!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
      return;
    }

    //TODO: API call to get request
    setLoading(true);
    const { SERVER_URL } = process.env;
    console.log(SERVER_URL);
    const rawResponse = await fetch(
      `https://kenken-backend-server.herokuapp.com/kenken`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(info),
      }
    );
    const data = await rawResponse.json();
    console.log(data);
    setModalOpen(!modalOpen);
    if (rawResponse.status == 200) {
      setCells(data);
      setLoading(false);
      toast.info("Created!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        width: "100%",
        margin: "auto",
        gap: "0px",
      }}
    >
      <ToastContainer />
      <Typography
        variant="h2"
        gutterBottom
        component="div"
        style={{ marginTop: "70px", marginBottom: "1px" }}
      >
        KenKen
      </Typography>
      <Stack spacing={5} direction="row" style={{ margin: "30px 0" }}>
        <Modal hanldeGenerate={hanldeGenerate} modalOpen={modalOpen} />
        <Button variant="contained" color="success" onClick={handleSubmit}>
          Submit
        </Button>
        <Button variant="contained" color="secondary" onClick={handleSolve}>
          Solve
        </Button>
      </Stack>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {loading ? (
          <Loading />
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${Math.sqrt(
                cells?.values.length
              )}, 85px)`,
              gridTemplateRows: `repeat(${Math.sqrt(
                cells?.values.length
              )}, 85px)`,
              gap: "0",
              rowGap: "0",
              columnGap: "0",
              width: "70%",
              height: "70%",
              justifyContent: "center",
              alignItems: "center",
              marginBottom: "200px",
            }}
          >
            {cells?.values.map((cell, i) => (
              <Cell
                key={i}
                cell={cell}
                solve={solve}
                answer={cells.result[i]}
                id={i}
                handleOnChange={handleOnChange}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
