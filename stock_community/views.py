from django.views.generic import TemplateView
import yfinance as yf

class StockIndexView(TemplateView):
    '''
    indices에 있는 차트 구현
    딕셔너리에 있는 값 불러와 yfinance로 1달 치 종가 자료
    time형을 str형으로 전환
    여러 차트를 불러오기 위해 딕셔너리로 딕셔너리로 지수 이름 : 종가로 chart_data 반환
    '''
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        indices = {
            'NASDAQ': '^IXIC',
            'SP_500': '^GSPC',
            'Dow_Jones': '^DJI'
        }
        
        chart_data = {}
        
        for name, symbol in indices.items():
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            
            hist.index = hist.index.strftime('%Y-%m-%d')
            
            chart_data[name] = hist['Close'].to_dict()
        
        context['chart_data'] = chart_data
        return context