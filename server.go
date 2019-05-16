package main

import (
    "strings"
    "net/http"
	"log"
	"fmt"
	"encoding/json"
	"github.com/gorilla/mux"
	"io/ioutil"
	//"github.com/tomasen/realip"
)

type player struct {
	ip string `json:"Ip"`
	Xl int `json:"Xl"`
	Yl int `json:"Yl"`
	Xg int `json:"Xg"`
	Yg int `json:"Yg"`
	Active string `json:"Active"`
}
type ipList struct {
	P1 player `json:"P1"`
	P2 player `json:"P2"`
	P3 player `json:"P3"`
	P4 player `json:"P4"`
}



type msg struct {
	Id string
	Content string
}

var ips ipList
var players int
var newmsg player
func serve(w http.ResponseWriter, req *http.Request) {
	players += 1
	inip := strings.Split(req.RemoteAddr, ":")[0]
	inip = strings.Split(inip, "\n")[0]
	//if ip == "127.0.0.1" {fmt.Println(ips.ip1)}
	switch players {
	case 0:
		ips.P1.ip = inip
		ips.P1.Active = "Y"
	case 1:
		ips.P2.ip = inip
		ips.P2.Active = "Y"
	case 2:
		ips.P3.ip = inip
		ips.P3.Active = "Y"
	case 3: 
		ips.P4.ip = inip
		ips.P4.Active = "Y"
	}
	
}

func setup(w http.ResponseWriter, req *http.Request){
	inip := strings.Split(req.RemoteAddr, ":")[0]
	inip = strings.Split(inip, "\n")[0]
	
	switch {
	case inip == ips.P1.ip:
		newmsg := player{ips.P1.ip, 0,players,0,0, "Y"}
		f, err := json.Marshal(&newmsg)
		if err != nil {
			fmt.Println("nup")
		}
		w.Write(f)
	case inip == ips.P2.ip:
		newmsg := player{ips.P2.ip, 0,players,0,0, "Y"}
		f, err := json.Marshal(&newmsg)
		if err != nil {
			fmt.Println("nup")
		}
		w.Write(f)
	case inip == ips.P3.ip:
		newmsg := player{ips.P3.ip, 0,players,0,0, "Y"}
		f, err := json.Marshal(&newmsg)
		if err != nil {
			fmt.Println("nup")
		}
		w.Write(f)
	case inip == ips.P4.ip:
		newmsg := player{ips.P4.ip, 0,players,0,0, "Y"}
		f, err := json.Marshal(&newmsg)
		if err != nil {
			fmt.Println("nup")
		}
		w.Write(f)
	}
	fmt.Println("we're here")
	
	
}
type test_struct struct {
    Test string
}

//This is how each client will send coodinates to the server, the server then will want to update each ip with the coordinates
func sendcoords(w http.ResponseWriter, req *http.Request){
	inip := strings.Split(req.RemoteAddr, ":")[0]
	inip = strings.Split(inip, "\n")[0]

	body, err := ioutil.ReadAll(req.Body)
    if err != nil {
        panic(err)
    }
    err = json.Unmarshal(body, &newmsg)
    if err != nil {
        panic(err)
	}

	switch inip {
	case ips.P1.ip:
		ips.P1.Xl = newmsg.Xl
		ips.P1.Yl = newmsg.Yl
	case ips.P2.ip:
		ips.P2.Xl = newmsg.Xl
		ips.P2.Yl = newmsg.Yl
	case ips.P3.ip:
		ips.P3.Xl = newmsg.Xl
		ips.P3.Yl = newmsg.Yl
	case ips.P4.ip:
		ips.P4.Xl = newmsg.Xl
		ips.P4.Yl = newmsg.Yl
	}

	//fmt.Println(newmsg.Xl)
	//fmt.Println(newmsg.Yl)
}

func recvcoords(w http.ResponseWriter, req *http.Request){
	f, err := json.Marshal(ips)
	if err != nil {
		fmt.Println("Error Sending Coords")
	}
	//fmt.Println(f)
	w.Write(f)
}

func main() {
	players = -1
	r := mux.NewRouter()
	r.HandleFunc("/", serve)
	r.HandleFunc("/setup", setup)
	r.HandleFunc("/sendcoords", sendcoords)
	r.HandleFunc("/recvcoords",recvcoords)
	http.Handle("/", r)
	
	err := http.ListenAndServe(":8000", nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
	}
	
}
