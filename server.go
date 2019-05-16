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
}
type ipList struct {
	p1 player
	p2 player
	p3 player
	p4 player
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
	ips.p1.ip = inip
	//if ip == "127.0.0.1" {fmt.Println(ips.ip1)}
	switch players {
	case 1:
		ips.p1.ip = inip
	case 2:
		ips.p2.ip = inip
	case 3:
		ips.p3.ip = inip
	case 4: 
		ips.p4.ip = inip
	}
	
}

func setup(w http.ResponseWriter, req *http.Request){
	inip := strings.Split(req.RemoteAddr, ":")[0]
	inip = strings.Split(inip, "\n")[0]
	
	switch {
	case inip == ips.p1.ip:
		newmsg := player{ips.p1.ip, 0,players,0,0}
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

func thing(w http.ResponseWriter, req *http.Request){
	body, err := ioutil.ReadAll(req.Body)
    if err != nil {
        panic(err)
    }
    //log.Println(string(body))
    //var t test_struct
    err = json.Unmarshal(body, &newmsg)
    if err != nil {
        panic(err)
	}
	fmt.Println(newmsg.Xl)
	fmt.Println(newmsg.Yl)
}


func main() {
	players = -1
	r := mux.NewRouter()
	r.HandleFunc("/", serve)
	r.HandleFunc("/setup", setup)
	r.HandleFunc("/coords", thing)
	http.Handle("/", r)
	
	err := http.ListenAndServe(":8000", nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
	}
	
}
