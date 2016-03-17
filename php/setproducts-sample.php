<?php
/**
 *  Przykladowy program w PHP przedstawiajacy wykorzystanie API IAI-Shop.com do edycji danych produktow
 *
 *  Poniższy program stanowi przyklad wykorzystania jednej z bramek API sluzacej do edycji produktu i ma
 *  on na celu zobrazowanie sposobu korzystania z API SOAP udostepnianego przez system IAI-Shop.com.
 *  Aby sprawdzic dzialanie programu wprowdzic dane do swojego panelu sklepu (nazwa sklepu, login oraz haslo)
 *  w sekcji konfiguracyjnej skryptu oraz odpowiednio zmodyfikowac dane produktow takiej jak ID oraz kod
 *  zewnetrznego systemu.
 *  UWAGA! Poniewaz ponizszy program modyfikuje stany magazynowe produktow, przykladowy skrypt nalezy wywolac
 *  dla produktow testowych (dodanych w panelu dla celow przeprowadzenia testow API)
 */

// Parametry konfiguracyjne skryptu (do uzupelnienia):
define('SHOP_NAME', 'markartur'); // nazwa sklepu (dla sklepu http://test1.iai-shop.com nalezy podac nazwe: test1)
define('PANEL_LOGIN', 'login'); // login do panelu sklepu
define('PANEL_PASS', 'password'); // haslo do panelu sklpeu

// utworzenie obiektu klienta SOAP
$objSoapClient = new SoapClient('http://' . SHOP_NAME . '.iai-shop.com/edi/api-setproducts.php?wsdl', array('location' => 'http://' . SHOP_NAME . '.iai-shop.com/edi/api-setproducts.php', 'trace' => 1));

// tablica parametrow wywolania bramki api
$request = array( 
    'setProducts' => array(
        // dane do uwierzytelnienia 
        'authenticate' => array(
            'system_key' => sha1(date('Ymd') . sha1(PANEL_PASS)), // klucz wygenerowany na podstawie hasla i daty
            'system_login' => PANEL_LOGIN // login uzytkownika do panelu sklepu
            ),
        // tablica parametrow
        'params' => array (
            // tablica ustawien konfiguracyjnych wywolania bramki
            'settings' => array (
                'modification_type' => 'edit' // tylko edycja produktu (nie pozwala na dodawanie nowych produktow)
            ),
            // tablica produktow do edycji
            'products' => array(
                // edycja stanu magazynowego oraz ceny produktu
                // identyfikowanego po id produktu oraz id rozmiaru
                array (
                    'id' => 1175014091, // identyfikator produktu (nalezy podac wlasciwy dla jednego z prdodktow z wlasneogo panelu)
                    'retail_price' => 22.50, // cena detaliczna brutto
                    // tablica danych rozmiarowych
                    'sizes' => array (
                        array (
                            'size_id' => 'uniw', // identyfikator rozmiaru
                            // tablica stanow magazynowych (ilosci produktu)
                            'quantity' => array (
                                // tablica magazynow
                                'stocks' => array ( 
                                    array (
                                        'stock_id' => 1, // id magazynu
                                        'quantity' => 10, // nowy stan magazynowy (ilosc)
                                    ),
                                    array (
                                        'stock_id' => 2, // id magazynu
                                        'quantity_add' => 5, // dodanie do aktualnej ilości 5 sztuk (powiększenie stanu magazynowego)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
);

// wywolanie bramki api setProducts
$response = $objSoapClient->__soapCall('setProducts', $request);

echo $objSoapClient->__getLastRequest();
// wyswietlenie wynikow zwroconych prze bramke
// print_r($response) 
?>