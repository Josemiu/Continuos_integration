import math

# Definiciones de costos y opciones del sistema
MEMBERSHIP_PLANS = {
    "basic": 50,
    "premium": 100, # Nota: La membresía 'premium' base NO es lo mismo que las 'premium_features'
    "family": 120,
}

ADDITIONAL_FEATURES = {
    "personal_training": 35,
    "group_classes": 20,
    "pool_access": 15,
    "exclusive_facilities": 40, # Característica Premium 
    "specialized_training": 50, # Característica Premium 
}

PREMIUM_FEATURES_LIST = ["exclusive_facilities", "specialized_training"]
DISCOUNT_GROUP_RATE = 0.10 # 10% de descuento para membresías grupales 
SURCHARGE_PREMIUM_RATE = 0.15 # 15% de recargo por características premium


class MembershipManager:
    """
    Gestiona el cálculo de costos, descuentos y validaciones del sistema de membresías.
    """
    def __init__(self):
        # Asunción: Los planes y características están disponibles por defecto.
        # En un sistema real, se usaría una base de datos para la validación
        pass

    def calculate_cost(self, plan_key: str, features: list, num_members: int, confirmed: bool) -> int:
        """
        Calcula el costo total de la membresía con descuentos y recargos.

        Args:
            plan_key (str): Llave del plan seleccionado (ej. 'basic').
            features (list): Lista de características adicionales seleccionadas.
            num_members (int): Número de miembros que se inscriben (para descuento grupal).
            confirmed (bool): Si el usuario confirmó la compra (Req. 8).

        Returns:
            int: Costo total redondeado a entero positivo, o -1 si es inválido/cancelado (Req. 9).
        """
        # ----------------------------------------------------
        # 1. Validación de Entrada y Confirmación (Req. 7, 9, 10)
        # ----------------------------------------------------
        if not confirmed:
            print("MENSAJE DE ERROR: El plan fue cancelado por el usuario.")
            return -1

        if num_members <= 0:
            print("MENSAJE DE ERROR: El número de miembros debe ser un entero positivo.")
            return -1

        if plan_key not in MEMBERSHIP_PLANS:
            print(f"MENSAJE DE ERROR: El plan '{plan_key}' no está disponible.")
            return -1

        for feature in features:
            if feature not in ADDITIONAL_FEATURES:
                print(f"MENSAJE DE ERROR: La característica adicional '{feature}' no está disponible.")
                return -1

        # ----------------------------------------------------
        # 2. Cálculo de Costos Base 
        # ----------------------------------------------------
        
        # Costo total de la membresía base (por miembro)
        base_cost = MEMBERSHIP_PLANS[plan_key]

        # Costo total de las características adicionales (por miembro)
        features_cost = sum(ADDITIONAL_FEATURES[f] for f in features)

        # Costo total antes de descuentos/recargos (por miembro)
        sub_total = base_cost + features_cost
        
        # Costo total inicial para todos los miembros
        total_cost = sub_total * num_members
        
        # Inicializar variables de descuentos y recargos
        total_discount = 0
        total_surcharge = 0
        
        # ----------------------------------------------------
        # 3. Recargo por Características Premium 
        # ----------------------------------------------------
        has_premium_feature = any(f in PREMIUM_FEATURES_LIST for f in features)
        
        if has_premium_feature:
            surcharge_amount = total_cost * SURCHARGE_PREMIUM_RATE
            total_surcharge += surcharge_amount
            # El recargo se aplica al subtotal antes de otros descuentos
            total_cost += total_surcharge
        
        # ----------------------------------------------------
        # 4. Descuento por Grupo 
        # ----------------------------------------------------
        if num_members >= 2:
            group_discount = total_cost * DISCOUNT_GROUP_RATE
            total_discount += group_discount
            print(f"NOTIFICACIÓN: Se aplicó un 10% de descuento grupal. Ahorro: ${group_discount:,.2f}")
            total_cost -= group_discount

        # ----------------------------------------------------
        # 5. Descuentos por Oferta Especial 
        # ----------------------------------------------------
        
        # El descuento especial se aplica al costo total, que incluye el recargo si aplica.
        special_offer_discount = 0
        if total_cost > 400:
            special_offer_discount = 50
        elif total_cost > 200:
            special_offer_discount = 20
        
        if special_offer_discount > 0:
            total_discount += special_offer_discount
            total_cost -= special_offer_discount
            print(f"NOTIFICACIÓN: Se aplicó un descuento por oferta especial de ${special_offer_discount:,.2f}")
            
        # ----------------------------------------------------
        # 6. Salida Final 
        # ----------------------------------------------------
        
        # Aseguramos que el resultado sea un entero y positivo.
        if total_cost < 0:
            return 0 # Si el costo es negativo debido a descuentos, lo dejamos en 0.
            
        return math.ceil(total_cost) # Redondeamos al entero superior más cercano (ceil)
