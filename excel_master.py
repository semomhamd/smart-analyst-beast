# زرار واتساب احترافي بالأيقونة واللون الأصلي
        import urllib.parse
        msg = urllib.parse.quote("يا وحش! تقرير MIA8444 المنسق والمنظم جاهز للمراجعة.")
        
        # كود HTML لعرض الزرار بالأيقونة
        whatsapp_btn = f"""
            <a href="https://wa.me/?text={msg}" target="_blank" style="text-decoration: none;">
                <div style="
                    background-color: #25D366;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    display: flex;
                    align-items: center;
                    width: fit-content;
                    font-weight: bold;
                    gap: 10px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                ">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20px">
                    Share on WhatsApp
                </div>
            </a>
        """
        st.markdown(whatsapp_btn, unsafe_allow_html=True)
