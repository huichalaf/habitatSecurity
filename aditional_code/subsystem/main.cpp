#include <mysql/mysql.h> /* libreria que nos permite hacer el uso de las conexiones y consultas con MySQL */
#include <iostream>
#include <string>

using namespace std;

class Connection {

	const char* HOSTNAME;
	const char* DATABASE;
	const char* USERNAME;
	const char* PASSWORD;
	const char* SOCKET;
	const int PORT = 3306;
	const int OPT = 0;

	MYSQL *CONN;
	MYSQL_RES *RES;
	MYSQL_ROW ROW;

	public:
		Connection();
		bool ejecucion(const char *input_mysql);
};

Connection::Connection(){
	HOSTNAME = "localhost";
	DATABASE = "USUARIOS";
	USERNAME = "papo";
	PASSWORD = "6pjrQ18auqxVAYw80drvqmpKPdBqc399oV9kÑ-15";
	SOCKET = NULL;

}

bool Connection::ejecucion(const char *input_mysql){
	try{
		
		CONN = mysql_init(NULL);
		
		if (!mysql_real_connect(CONN, HOSTNAME, USERNAME, PASSWORD, DATABASE, PORT, SOCKET, OPT)){
			cerr<<mysql_error(CONN)<<endl;
		}
		
		if (mysql_query(CONN, input_mysql)){
			cerr<<mysql_error(CONN)<<endl;
			return false;
		}

		RES = mysql_use_result(CONN);
		//cout<<"*** MYSQL - SHOW TABLES *** =>"<<DATABASE<<endl;

		while((ROW = mysql_fetch_row(RES))!=NULL){
			cout<<ROW[0]<<endl;	
		}

		mysql_free_result(RES);
		mysql_close(CONN);

		return true;

	}catch(char *e){
		cerr<<"[EXCEPTION] "<<e<<endl;
		return false;
	}
}

void cli(){

	string mensaje_de_salida = "exit";
	Connection objConn;
	string mensaje;
	bool result = false;

	while(true){
		
		cout<<"MYSQL; ";getline(cin>>ws, mensaje);
		cout<<mensaje;
		if(mensaje == mensaje_de_salida) break;
		result = objConn.ejecucion(mensaje.c_str());

		if(!result) cout<<"ERROR"<<endl;
	}
}

int main(){

	int opcion = 0;
	cout<<"\n\tBienvenido Administrador";

	try{
		while(true){
			
			cout<<"\n1.- añadir usuarios";
			cout<<"\n2.- eliminar usuarios";
			cout<<"\n3.- añadir condominios";
			cout<<"\n4.- eliminar condominios";
			cout<<"\n5.- interactuar con la consola de mysql";
			cout<<"\nIngrese su opción: ";cin>>opcion;

			switch(opcion){
				case 1:
				case 2:
				case 3:
				case 4:
				case 5: cli();
			}
		}
	}catch(char *e){
		
		cerr<<"[EXCEPTION] "<<e<<endl;
		return false;
	
	}
}