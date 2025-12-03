import time
#Descriptif :
#chaque carte à une valeur entre 1 et 11
#Si la main comporte un ou plusieurs As :
# - on ajoute 10 à la main en +.
#    - la main possède désormais 2 valeurs : la somme normal et la somme de +10
# - si la somme max des deux dépasse 21 :
#   - on garde seulement la somme min < 21

t0 = time.perf_counter()


t1 = time.perf_counter()
print(f"temps d'execution de valeur() : {t1 - t0:.6f} secondes")