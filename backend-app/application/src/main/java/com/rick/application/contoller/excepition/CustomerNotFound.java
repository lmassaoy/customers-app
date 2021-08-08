package com.rick.application.contoller.excepition;

public class CustomerNotFound extends RuntimeException{

    private static final long serialVersionUID = 1869300553614629710L;

    public CustomerNotFound(String mensagem){
        super (mensagem);
    }

    public CustomerNotFound(String mensagem, Throwable causa){
        super(mensagem,causa);
    }
}
