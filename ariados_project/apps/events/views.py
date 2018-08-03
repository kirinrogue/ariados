import dryscrape
from bs4 import BeautifulSoup
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ariados.models import Event
from .serializers import EventSerializer


# View que será llamada periódicamente para crear los eventos necesarios automáticamente a través de la web
# oficial de Pokémon GO! mediante web scrapping , ya que no disponemos de API oficial.
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_pgo_events(request):
    # eventos:
    # events-list__event__date__day : clase para los días (span)
    # events-list__event__date__month : clase para el mes
    # events-list__event__content (CONTENIDO, DIVIDIO POR TITULO Y TEXTO)
    # events-list__event__title : clase para el título del evento
    # events-list__event__body : cuerpo / descripción del evento
    sess = dryscrape.Session()
    sess.visit('https://pokemongolive.com/en/events/')
    body = sess.body()

    soup = BeautifulSoup(body)
    dias = list(soup.find_all('span', class_='events-list__event__date__day'))
    meses = list(soup.find_all('span', class_='events-list__event__date__month'))
    titulos = list(soup.find_all('div', class_='events-list__event__title'))
    descripciones = list(soup.find_all('div', class_='events-list__event__body'))

    if dias and meses and titulos and descripciones:
        for i in range(5):
            if not Event.objects.filter(days=dias[i].text, title=titulos[i].text).exists():
                Event.objects.create(title=titulos[i].text, description=descripciones[i].text,
                                     days=dias[i].text + ' ' + meses[i].text)

    return HttpResponse('Got them!')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_last_events(request):
    try:
        events = Event.objects.all().order_by('-id')[0:3]
        serializer = EventSerializer(events, many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)
