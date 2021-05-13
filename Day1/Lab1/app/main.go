package main

import (
    "fmt"
	"database/sql"
	"net/http"
	"encoding/json"
	"io/ioutil"
	"os"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

type psqlInfo struct {
	HOST   string `json:"HOST"`
	PORT    string `json:"PORT"`
	DBNAME   string `json:"DBNAME"`
	USER string `json:"USER"`
	PASS string `json:"PASS"`
	SSLMODE string `json:"SSLMODE"`
}

var input_file string

type record struct {
	id          int
	name, bdate string
}

func show(db *sql.DB) ([]record, error) {
	rows, err := db.Query("SELECT * FROM lab1_db")
	
	if err != nil {
		return nil, nil
	}
	defer rows.Close()

	var rec_array = make([]record, 0)
	var rec record

	for rows.Next() {
		err = rows.Scan(&rec.id, &rec.name, &rec.bdate)
		if err != nil {
			return nil, nil
		}
		rec_array = append(rec_array, rec)
	}
	err = rows.Err()
	if err != nil {
		return nil, nil
	}
	
	fmt.Println(rec_array[0])
	
	return rec_array, nil
}
	
func get_dbAccessInfo() string {

		jsonFile, err := os.Open(input_file)
		if err != nil {
			panic(err)
		}
		defer jsonFile.Close()

		var result psqlInfo

		byteValue, _ := ioutil.ReadAll(jsonFile)

		if err := json.Unmarshal(byteValue, &result); err != nil {
			panic(err)
		}

		dbaccess_msg := fmt.Sprintf("host=%s port=%s dbname=%s sslmode=%s user=%s password=%s ",
			result.HOST,
			result.PORT,
			result.DBNAME,
			result.SSLMODE,
			result.USER,
			result.PASS)

		return dbaccess_msg
	}

	func main() {
		input_file = "/go/bin/dbcred.json"
		psqlInfo := get_dbAccessInfo()
		
		fmt.Println(psqlInfo)

		db, err := sql.Open("postgres", get_dbAccessInfo())
		if err != nil{
			panic(err)
		}
		defer db.Close()

		r := mux.NewRouter()

		r.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			arr, _ := show(db)

			str := "<table border=1><caption><h2>Birthday list</h2>\n</caption><tr><th>Full Name</th><th>Date</th></tr>\n"
			for i:=0; i<len(arr) ; i++{
				str += "<tr><td>"+arr[i].name+"</td><td>"+arr[i].bdate[:10]+"</td></tr>\n"
			} 
			str += "</table>"

			fmt.Fprintf(w, str)})
		
		r.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
			fmt.Fprintf(w, "<h1>Running...\n</h1> <table>{{range .}}<tr><td>{{.}}</td></tr>{{end}}</table>")})

    	http.ListenAndServe(":80", r)

		return
	}