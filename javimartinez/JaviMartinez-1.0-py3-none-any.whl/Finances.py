def dfStock(company,init,final=0):
    from datetime import date
    import yfinance as yf
    
    if(final==0):
        final=date.today().strftime("%Y-%m-%d")
    
    df=yf.Ticker(company).history(period='1d',start=init,end=final)
    
    return df

def candles(company,init,final=0):
    from datetime import date
    import yfinance as yf
    import mplfinance as mpf
    
    if(final==0):
        final=date.today().strftime("%Y-%m-%d")
    
    df=yf.Ticker(company).history(period='1d',start=init,end=final)
    
    mpf.plot(df,type='candle',style='charles',volume=True,ylabel='Precio',ylabel_lower='Volumen',
         title="Stock de {}".format(company),mav=(3,6,9))